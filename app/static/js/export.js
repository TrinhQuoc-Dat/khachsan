document.getElementById('export-btn').addEventListener('click', function () {
      // Lấy năm được chọn từ combobox
      const yearSelector = document.getElementById('yearSelector');
      const selectedYear = yearSelector.value;

      // Tạo tên file dựa trên năm được chọn
      const suggestedName = `BaoCaoTongQuan_${selectedYear}.xlsx`;

      // Lấy dữ liệu từ bảng
      const table = document.querySelector('.statistic-table');
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