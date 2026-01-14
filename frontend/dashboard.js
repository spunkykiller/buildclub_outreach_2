const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        const authors = ref([]);
        const stats = ref({ emails_sent_today: 0, pending_emails: 0 });
        const discoveryQuery = ref("Founders who wrote a book");
        const showUpload = ref(false);
        const selectedAuthor = ref(null);
        const fileInput = ref(null);

        const fetchAuthors = async () => {
            const res = await fetch('/authors');
            authors.value = await res.json();

            const statsRes = await fetch('/stats');
            stats.value = await statsRes.json();
        };

        const badgeClass = (active) => {
            return active ? 'opacity-100 grayscale-0' : 'opacity-25 grayscale';
        };

        const runDiscovery = async () => {
            alert("Discovery started! Takes a few minutes.");
            await fetch(`/discover?query=${encodeURIComponent(discoveryQuery.value)}`, { method: 'POST' });
            setTimeout(fetchAuthors, 2000);
        };

        const openUpload = (author) => {
            selectedAuthor.value = author;
            showUpload.value = true;
        };

        const submitUpload = async () => {
            if (!fileInput.value.files[0]) return;
            const formData = new FormData();
            formData.append('file', fileInput.value.files[0]);

            await fetch(`/upload_pdf/${selectedAuthor.value.id}`, {
                method: 'POST',
                body: formData
            });
            showUpload.value = false;
            fetchAuthors();
        };

        const analyze = async (id) => {
            await fetch(`/analyze/${id}`, { method: 'POST' });
            alert("Analysis queued!");
            fetchAuthors();
        };

        const generate = async (id) => {
            await fetch(`/generate_email/${id}`, { method: 'POST' });
            fetchAuthors();
        };

        const sendNext = async () => {
            const res = await fetch('/send_next', { method: 'POST' });
            const data = await res.json();
            alert(data.status);
            fetchAuthors();
        };

        const toggleStatus = async (author, field, value) => {
            // Optimistic update
            author.pipeline[field] = value;

            try {
                await fetch(`/update_outreach_status/${author.id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ field, value })
                });
            } catch (e) {
                console.error(e);
                alert("Failed to update status");
                fetchAuthors(); // Revert on error
            }
        };

        onMounted(() => {
            fetchAuthors();
            setInterval(fetchAuthors, 2000); // Polling every 2s
        });

        return {
            authors, stats, discoveryQuery, showUpload, selectedAuthor, fileInput,
            fetchAuthors, badgeClass, runDiscovery, openUpload, submitUpload, analyze, generate, sendNext, toggleStatus
        };
    }
}).mount('#app');
