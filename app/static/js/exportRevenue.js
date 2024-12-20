document.addEventListener('DOMContentLoaded', function () {
      document.getElementById('export-btn').addEventListener('click', function () {
            // Lấy tháng và năm được chọn từ combobox
            const monthPicker = document.getElementById('monthPicker');
            const selectedMonth = monthPicker ? monthPicker.value : 'UnknownMonth';
            const revenue = document.querySelector('.revenue');

            // Tạo tên file dựa trên tháng và năm được chọn
            let suggestedName;
            if (revenue) {
                  suggestedName = `BaoCaoDoanhThu_${selectedMonth}.xlsx`;
            } else {
                  suggestedName = `BaoCaoMatDo_${selectedMonth}.xlsx`;
            }

            // Lấy dữ liệu từ bảng
            const table = document.querySelector('.report-table');
            if (!table) {
                  console.error('Table not found');
                  return;
            }

            const rows = table.querySelectorAll('tr');
            const reportData = [];

            rows.forEach(row => {
                  const cells = row.querySelectorAll('th, td');
                  const rowData = [];
                  cells.forEach(cell => {
                        rowData.push(cell.innerText);
                  });
                  reportData.push(rowData);
            });

            // Tạo workbook và worksheet
            const wb = XLSX.utils.book_new();
            const ws = XLSX.utils.aoa_to_sheet(reportData);
            XLSX.utils.book_append_sheet(wb, ws, 'Report');

            // Xuất file
            XLSX.writeFile(wb, suggestedName);
      });
});