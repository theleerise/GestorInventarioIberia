function searchOnTable(search_box, table_id) {
  var busqueda = document.getElementById(search_box);
  var table = document.getElementById(table_id).tBodies[0];

  // Función para buscar en la tabla
  function buscaTabla() {
      var texto = busqueda.value.toLowerCase();
      var r = 0;
      while (row = table.rows[r++]) {
          if (row.innerText.toLowerCase().indexOf(texto) !== -1)
              row.style.display = null;
          else
              row.style.display = 'none';
      }
  }

  // Asocia el evento 'keyup' al campo de búsqueda
  busqueda.addEventListener('keyup', buscaTabla);
}
