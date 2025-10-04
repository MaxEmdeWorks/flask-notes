$(document).ready(function () {
    const NoteManager = {
        currentNote: {},

        // Initialize all modal handlers
        init() {
            this.bindViewModal();
            this.bindEditModal();
            this.bindEditFromView();
            this.bindClearSearch();
            this.bindArchivedToggle();
            this.bindCategoryFilter();
            this.initTooltips();
        },

        // Initialize tooltips
        initTooltips() {
            // Initialize all tooltips
            $('[data-bs-toggle="tooltip"]').tooltip();

            // Re-initialize tooltips when modals are shown
            $('.modal').on('shown.bs.modal', function () {
                $('[data-bs-toggle="tooltip"]').tooltip();
            });
        },

        // Extract note data from button element
        extractNoteData($button) {
            return {
                id: $button.data('note-id'),
                title: $button.data('note-title'),
                content: $button.data('note-content'),
                category: $button.data('note-category')
            };
        },

        // Populate edit modal with note data
        populateEditModal(noteData) {
            const updateUrl = $('#editForm').data('update-url').replace('/0', `/${noteData.id}`);
            $('#editForm').attr('action', updateUrl);
            $('#editNoteTitle').val(noteData.title);
            $('#editNoteContent').val(noteData.content);
            $('#editNoteCategory').val(noteData.category || 0);
        },

        // Handle view modal display
        bindViewModal() {
            $('#viewModal').on('show.bs.modal', (event) => {
                const noteData = this.extractNoteData($(event.relatedTarget));
                this.currentNote = noteData;
                $('#viewNoteTitle').text(noteData.title);
                $('#viewNoteContent').text(noteData.content);
            });
        },

        // Handle direct edit modal
        bindEditModal() {
            $('#editModal').on('show.bs.modal', (event) => {
                const $button = $(event.relatedTarget);
                if ($button.length) {
                    this.populateEditModal(this.extractNoteData($button));
                }
            });
        },

        // Handle edit from view modal
        bindEditFromView() {
            $('#editFromView').on('click', () => {
                $('#viewModal').modal('hide');
                setTimeout(() => {
                    this.populateEditModal(this.currentNote);
                    $('#editModal').modal('show');
                }, 300);
            });
        },

        // Handle clear search functionality
        bindClearSearch() {
            $('#clearSearch').on('click', () => {
                // Remove search parameters and go to base notes URL
                window.location.href = window.location.pathname;
            });
        },

        // Handle archived notes toggle
        bindArchivedToggle() {
            $('#archivedToggle').on('change', function () {
                const isChecked = $(this).is(':checked');
                const currentUrl = new URL(window.location);
                currentUrl.searchParams.set('archived', isChecked);
                currentUrl.searchParams.set('page', '1'); // Reset to first page
                window.location.href = currentUrl.toString();
            });
        },

        // Handle category filter
        bindCategoryFilter() {
            $('#categoryFilter').on('change', function () {
                $('#categoryFilterForm').submit();
            });
        }
    };

    // Initialize the note manager
    NoteManager.init();
});
