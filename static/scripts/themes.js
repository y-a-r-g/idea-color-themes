(function() {
    $(document).ready(function() {
        var $filterOrderSelect = $('.js-filter-order-select'),
            $filterOrderItem = $('.js-filter-order-item'),
            $filterName = $('.js-filter-name'),
            $applyFilterButton = $('.js-apply-filter'),

            applyFilter = function() {
                window.location.href = '/themes/?' + $.param({
                    order: $filterOrderSelect.data('order'),
                    filter: $filterName.val()
                });
                return false;
            };

        $filterOrderItem.click(function() {
            var $item = $(this);
            $filterOrderSelect.data('order', $item.data('order'));
            $filterOrderSelect.html($item.html() + '<span class="caret"></span>');
        });

        $applyFilterButton.click(applyFilter);

        $filterName.keypress(function(event) {
            if (event.which == 13) {
                applyFilter();
            }
        });
    });
})();
