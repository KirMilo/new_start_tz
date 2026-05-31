$(document).ready(function () {
        const API_URL = 'https://api.restful-api.dev/objects';
        let items = [];
        let filteredItems = [];

        const $tableBody = $('#items-table tbody');

        let currentSort = {field: null, direction: 'asc'}

        function fetchItems() {
            $.ajax({
                url: API_URL,
                method: 'GET',
                dataType: 'json',
                success: function (data) {
                    console.log(`It loaded ${data.length} items successfully!`)
                    items = data;
                    filteredItems = items.slice();
                    renderTable();
                },
                error: function (xhr, status, error) {
                    console.error(error);
                }
            });
        }

        function renderTable() {
            $tableBody.empty();
            if (!filteredItems.length) {
                $tableBody.append(
                    '<tr><td colspan="6">No data to show</td></tr>'
                );
                return;
            }

            filteredItems.forEach(function (item) {
                const itemData = item.data || {};
                const rowHtml = `
                <tr>
                    <td>${item.id || ''}</td>
                    <td>${item.name || ''}</td>
                    <td>${itemData.price || '-'}</td>
                </tr>
            `;
                $tableBody.append(rowHtml);
            });
        }

        function applySort() {
            if (!currentSort.field) return;

            filteredItems.sort(function (a, b) {
                let valA = a[currentSort.field] !== undefined ?
                    a[currentSort] : a.data === undefined || a.data === null ? undefined : a.data[currentSort.field];
                let valB = b[currentSort.field] !== undefined ?
                    b[currentSort] : b.data === undefined || b.data === null ? undefined : b.data[currentSort.field];

                const defaultValue = currentSort.direction === 'asc' ? Infinity : 0

                if (currentSort.field === 'price') {
                    valA = valA === undefined || valA === null || valA === '-' ? defaultValue : parseFloat(valA);
                    valB = valB === undefined || valB === null || valB === '-' ? defaultValue : parseFloat(valB);
                }
                if (valA < valB) return currentSort.direction === 'asc' ? -1 : 1;
                if (valA > valB) return currentSort.direction === 'asc' ? 1 : -1;
                return 0;
            });
        }

        function toggleSort(field) {
            if (currentSort.field === field) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.field = field;
                currentSort.direction = 'asc';
            }
            applySort();
            renderTable();
        }

        $('#items-table thead').on('click', 'th[data-sort]', function () {
            const field = $(this).data('sort');
            toggleSort(field);
        })

        fetchItems();
    }
)