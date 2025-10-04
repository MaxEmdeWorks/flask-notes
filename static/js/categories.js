$(document).ready(function () {
    const CategoryManager = {
        // Initialize all event handlers
        init() {
            this.bindColorPickers();
            this.bindEditCategory();
            this.bindSearch();
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

        // Handle color selection for both forms
        bindColorPickers() {
            // Create form color picker
            $('#categoryForm').on('click', '.color-option', function (e) {
                e.preventDefault();
                $('#categoryForm .color-option').removeClass('border-light border-3 shadow-sm').addClass('border-transparent border-2');
                $(this).removeClass('border-transparent border-2').addClass('border-light border-3 shadow-sm');
                $('#categoryForm input[name="color"]').val($(this).data('color'));
            });

            // Edit modal color picker
            $('#editCategoryModal').on('click', '.edit-color-option', function (e) {
                e.preventDefault();
                $('#editCategoryModal .edit-color-option').removeClass('border-light border-3 shadow-sm').addClass('border-transparent border-2');
                $(this).removeClass('border-transparent border-2').addClass('border-light border-3 shadow-sm');
                $('#editCategoryColor').val($(this).data('color'));
            });
        },

        // Handle edit category button clicks
        bindEditCategory() {
            $(document).on('click', '.edit-category-btn', function () {
                const categoryId = $(this).data('category-id');
                CategoryManager.loadCategoryData(categoryId);
            });
        },

        // Handle category search functionality
        bindSearch() {
            $('#clearSearch').on('click', function() {
                // Remove search parameters and go to base categories URL
                window.location.href = window.location.pathname;
            });
        },

        // Load category data via AJAX
        loadCategoryData(categoryId) {
            const getUrl = $('#editCategoryForm').data('get-url').replace('/0', `/${categoryId}`);
            $.ajax({
                url: getUrl,
                type: 'GET',
                success: function (data) {
                    CategoryManager.populateEditModal(data, categoryId);
                },
                error: function () {
                    console.error('Failed to load category data');
                }
            });
        },

        // Populate edit modal with category data
        populateEditModal(data, categoryId) {
            const updateUrl = $('#editCategoryForm').data('update-url').replace('/0', `/${categoryId}`);
            $('#editCategoryForm').attr('action', updateUrl);
            $('#editCategoryName').val(data.name);
            $('#editCategoryColor').val(data.color);
            $('#editCategoryModal .edit-color-option').removeClass('border-light border-3 shadow-sm').addClass('border-transparent border-2');
            $('#editCategoryModal .edit-color-option[data-color="' + data.color + '"]').removeClass('border-transparent border-2').addClass('border-light border-3 shadow-sm');
            $('#editCategoryModal').modal('show');
        }
    };

    // Initialize the category manager
    CategoryManager.init();
});
