const { createApp, ref, onMounted } = Vue;

createApp({
    setup() {
        const authors = ref([]);
        const stats = ref({ emails_sent_today: 0, pending_emails: 0 });
        const discoveryQuery = ref("Founders who wrote a book");
        const showUpload = ref(false);
        const selectedAuthor = ref(null);
        const fileInput = ref(null);

        // localStorage key for tracking
        const STORAGE_KEY = 'buildclub_outreach_tracking';

        // Load tracking data from localStorage
        const loadTrackingData = () => {
            try {
                const saved = localStorage.getItem(STORAGE_KEY);
                return saved ? JSON.parse(saved) : {};
            } catch (e) {
                console.error('Error loading tracking data:', e);
                return {};
            }
        };

        // Save tracking data to localStorage
        const saveTrackingData = (tracking) => {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(tracking));
            } catch (e) {
                console.error('Error saving tracking data:', e);
            }
        };

        const fetchAuthors = async () => {
            try {
                const res = await fetch('/authors');
                const authorsData = await res.json();

                // Load tracking from localStorage
                const tracking = loadTrackingData();

                // Merge server data with localStorage tracking
                authors.value = authorsData.map(author => {
                    const tracked = tracking[author.id] || {};
                    return {
                        ...author,
                        pipeline: {
                            ...author.pipeline,
                            // Override with localStorage values if they exist
                            connection_sent: tracked.connection_sent !== undefined ? tracked.connection_sent : author.pipeline.connection_sent,
                            dm_sent: tracked.dm_sent !== undefined ? tracked.dm_sent : author.pipeline.dm_sent,
                            response_status: tracked.response_status || author.pipeline.response_status
                        }
                    };
                });

                const statsRes = await fetch('/stats');
                stats.value = await statsRes.json();
            } catch (error) {
                console.error('Error fetching authors:', error);
            }
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
            // Optimistic update in UI
            author.pipeline[field] = value;

            // Load current tracking
            const tracking = loadTrackingData();

            // Update tracking for this author
            if (!tracking[author.id]) {
                tracking[author.id] = {};
            }
            tracking[author.id][field] = value;

            // Save to localStorage immediately
            saveTrackingData(tracking);

            // Try to update backend (optional - will fail gracefully on Vercel)
            try {
                await fetch(`/update_outreach_status/${author.id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ field, value })
                });
            } catch (e) {
                // Backend update failed, but localStorage already saved
                console.log('Backend update unavailable, using localStorage only');
            }
        };

        onMounted(() => {
            fetchAuthors();
            // Refresh less frequently to avoid overwhelming the (potentially serverless) backend
            setInterval(fetchAuthors, 10000); // Every 10 seconds instead of 2
        });

        return {
            authors, stats, discoveryQuery, showUpload, selectedAuthor, fileInput,
            fetchAuthors, badgeClass, runDiscovery, openUpload, submitUpload, analyze, generate, sendNext, toggleStatus
        };
    }
}).mount('#app');
