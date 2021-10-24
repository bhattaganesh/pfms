$(document).ready(function () {
  setTimeout(function () {
    $(".alert-dismissible").hide();
  }, 3000);
});

$(document).ready(function () {
  $(".select2").select2();
});


// ####################################### for single record deleting
$(".delete-btn").click(function (e) {
  e.preventDefault();
  // url = $(this).attr('data-url');
  // url = $(this).data('url');
  let form = $(this).parent().find("form");
  bootbox.confirm({
    title: "Delete Record?",
    message: "Are you sure you want to delete this data?",
    buttons: {
      cancel: {
        label: '<i class="fa fa-times"></i> Cancel',
      },
      confirm: {
        label: '<i class="fa fa-check"></i> Confirm',
      },
    },
    callback: function (result) {
      if (result) {
        form.submit();
      }
    },
  });
});

// ######################################## for single record deleting in search result table
function deleteRecord(id) {
  let form = $('#delForm' + id);
  console.log(form);
  bootbox.confirm({
    title: "Delete Record?",
    message: "Are you sure you want to delete this data?",
    buttons: {
      cancel: {
        label: '<i class="fa fa-times"></i> Cancel',
      },
      confirm: {
        label: '<i class="fa fa-check"></i> Confirm',
      },
    },
    callback: function (result) {
      if (result) {
        form.submit();
      }
    },
  });
}


// ################################### dark mode or light mode
var toggleSwitch = document.querySelector(
  '.theme-switch input[type="checkbox"]'
);
var currentTheme = localStorage.getItem("theme");
var mainHeader = document.querySelector(".main-header");

if (currentTheme) {
  if (currentTheme === "light") {
    if (document.body.classList.contains("dark-mode")) {
      document.body.classList.remove("dark-mode");
    }
    if (mainHeader.classList.contains("navbar-dark")) {
      mainHeader.classList.remove("navbar-dark");
      mainHeader.classList.add("navbar-light");
    }

    toggleSwitch.checked = false;
  }
}

function switchTheme(e) {
  if (e.target.checked) {
    if (document.body.classList.contains("dark-mode")) {
      document.body.classList.remove("dark-mode");
    }
    if (mainHeader.classList.contains("navbar-dark")) {
      mainHeader.classList.remove("navbar-dark");
      mainHeader.classList.add("navbar-light");
    }
    localStorage.setItem("theme", "light");
  } else {
    if (!document.body.classList.contains("dark-mode")) {
      document.body.classList.add("dark-mode");
    }
    if (!mainHeader.classList.contains("navbar-dark")) {
      mainHeader.classList.add("navbar-dark");
      mainHeader.classList.remove("navbar-light");
    }
    localStorage.setItem("theme", "dark");
  }
}

toggleSwitch.addEventListener("change", switchTheme, false);


// ####################################### searching functionality for records

const searchUrl = $('#searchField').parent().attr('action');
var tableName = $('#resultTable').data('table-name');
var page_n = '';
// console.log(searchUrl);
$('#resultTable').find('.pagination').find('a').click(function (event) {
  event.preventDefault();
  page_n = $(this).attr('href').split('page=')[1];;
});
$('#searchField').keyup(function (e) {
  const searchStr = e.target.value;
  if (searchStr.trim().length > 0) {
    $('#resultTable').find('.pagination').addClass('d-none');
    // console.log(searchStr);
    var tbody = '';
    fetch(searchUrl, {
      body: JSON.stringify({
        'searchStr': searchStr,
        'page_n': page_n
      }),
      method: "POST"
    })
      .then((res) => res.json())
      .then((result) => {
        console.log(result);
        var csrfToken = $('#csrfParent').parent().find("input[type='hidden']").val();
        $('#resultTable').removeClass('d-none');
        $('#mainTable').addClass('d-none');
        if (result.length) {
          $('#resultTable').find('.controls').removeClass('d-none');
          $('#resultTable').find('thead').removeClass('d-none');
          $('#resultTable').find('tbody').find('h1').addClass('d-none');
          result.forEach((item, key) => {
            tbody += `
          <tr>
            <td>
              <div class="icheck-primary">
                <input type="checkbox" value="" id="check1">
                <label for="check1"></label>
              </div>
            </td>
            <td>${++key}</td>
            <td>${parseFloat(item.amount).toFixed(1)}</td>
            <td>${item.category_title}</td>
            <td>${truncateChars(item.description)}</td>
            <td>${item.date}</td>
            <td>${item.entry_date}</td>
            <td>
              <a href="/${tableName}s/details/${item.id}/" title="View this ${tableName}" class="mr-2 btn btn-sm btn-primary"><i class="fa fa-eye" aria-hidden="true"></i></a>
              <a href="/${tableName}s/edit/${item.id}/" title="Edit this Income" class="mr-2 btn btn-sm btn-success"><i class="fa fa-edit" aria-hidden="true"></i></a>
              <a href="javascript:;" onclick="deleteRecord('${item.id}');" title="Delete this Income" class="  btn btn-sm btn-danger delete-btn"><i class="fa fa-trash" aria-hidden="true"></i></a>
              <form action="/${tableName}s/delete/${item.id}/" id="delForm${item.id}" method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
              </form>
            </td>
          </tr>`
          });
          $('#resultTable').find('tbody').html(tbody);
        } else {
          $('#resultTable').find('.controls').addClass('d-none');
          $('#resultTable').find('thead').addClass('d-none');
          $('#resultTable').find('tbody').html(`<h1 class='text-center m-4'>No results found!</h1>`);
        }
      });
  } else {
    $('#mainTable').removeClass('d-none');
    $('#resultTable').addClass('d-none');
  }
});


// ################################################# for trunacting chars

function truncateChars(str, len = 19, ending = '...') {
  if (str.length <= len) {
    return str;
  }
  else {
    return (str.substring(0, len) + ending);
  }
}


//  ########################################## for refresshing window

$('.fa-sync-alt').parent().on('click', () => {
  window.location.reload(true);
});



// ############################ for deleting multiple records

$('.fa-trash-alt').parent().click((e) => {
  let selected_record = [];
  $.each($("input:checkbox[name='chk_record']:checked"), function () {
    selected_record.push($(this).val());
  });
  if (selected_record.length) {
    $('.fa-trash-alt').parent().find('form').find("input[name='ids']").val(selected_record);
    let multipleDelform = $('.fa-trash-alt').parent().find('form');
    bootbox.confirm({
      title: "Delete Record?",
      message: "Are you sure you want to delete this data?",
      buttons: {
        cancel: {
          label: '<i class="fa fa-times"></i> Cancel',
        },
        confirm: {
          label: '<i class="fa fa-check"></i> Confirm',
        },
      },
      callback: function (result) {
        if (result) {
          multipleDelform.submit();
        }
      },
    });
  } else {
    bootbox.alert({
      message: "You must select at-least one record!",
      backdrop: true
    });
  }
});

// ################################## for databale customization and initialization

var _target_chars = 40
var _target_col = [2,3]
$(function () {
  let copyButtonTrans = 'Copy'
  let csvButtonTrans = 'CSV'
  let excelButtonTrans = 'Excel'
  let pdfButtonTrans = 'PDF'
  let printButtonTrans = 'Print'
  let colvisButtonTrans = 'Column visibility'

  // let languages = {
  //   'en': 'https://cdn.datatables.net/plug-ins/1.10.19/i18n/English.json'
  // };

  $.extend(true, $.fn.dataTable.Buttons.defaults.dom.button, { className: 'btn btn-default btn-sm' })
  $.extend(true, $.fn.dataTable.defaults, {
    // language: {
    //   url: languages['en']
    // },
    columnDefs: [
      {
        orderable: false,
        className: 'select-checkbox',
        targets: 0
      },
      {
        orderable: false,
        targets: -1
      },
      {
        targets: _target_col,
        render: $.fn.dataTable.render.ellipsis( _target_chars, true )
      },
    ],
    select: {
      style: 'multi+shift',
      selector: 'td:first-child'
    },
    order: [],
    scrollX: true,
    pageLength: 100,
    dom: 'lBfrtip<"actions">',
    buttons: [
      {
        extend: 'copy',
        className: 'btn-default',
        text: copyButtonTrans,
        exportOptions: {
          columns: ':visible'
        }
      },
      {
        extend: 'csv',
        className: 'btn-default',
        text: csvButtonTrans,
        exportOptions: {
          columns: ':visible'
        }
      },
      {
        extend: 'excel',
        className: 'btn-default',
        text: excelButtonTrans,
        exportOptions: {
          columns: ':visible'
        }
      },
      {
        extend: 'pdf',
        className: 'btn-default',
        text: pdfButtonTrans,
        exportOptions: {
          columns: ':visible'
        }
      },
      {
        extend: 'print',
        className: 'btn-default',
        text: printButtonTrans,
        exportOptions: {
          columns: ':visible'
        }
      },
      {
        extend: 'colvis',
        className: 'btn-default',
        text: colvisButtonTrans,
        exportOptions: {
          columns: ':visible'
        }
      }
    ]
  });

  //$.fn.dataTable.ext.classes.sPageButton = 'btn btn-xs btn-primary';
});


const _token = document.querySelector("input[name='csrfmiddlewaretoken']").value;
$(function () {
  let dtButtons = $.extend(true, [], $.fn.dataTable.defaults.buttons)
  let deleteButtonTrans = 'Delete selected'
  let deleteButton = {
    text: deleteButtonTrans,
    className: 'btn-danger mul-del-cat',
    url: $('#multipleCatDelForm').data('del-url'),
    action: function (e, dt, node, config) {
      var ids = $.map(dt.rows({ selected: true }).nodes(), function (entry) {
        return $(entry).data('entry-id')
      });
      //console.log(Object.keys(ids).map(function(k){return ids[k]}).join(","));
      var newids = Object.keys(ids).map(function (k) { return ids[k] }).join(",");
      if (ids.length === 0) {
        bootbox.alert({
          message: "You must select at-least one record!",
          backdrop: true
        });
        return
      }
      bootbox.confirm({
        title: "Delete Record?",
        message: "Are you sure you want to delete this data?",
        buttons: {
          cancel: {
            label: '<i class="fa fa-times"></i> Cancel',
          },
          confirm: {
            label: '<i class="fa fa-check"></i> Confirm',
          },
        },
        callback: function (result) {
          if (result) {
            $.ajax({
              method: 'POST',
              url: config.url,
              data: { "ids": newids, 'csrfmiddlewaretoken': _token },
              success:function (res) { 
                console.log(res);
                if (res.status){
                  bootbox.alert(`${res.msg}`, function () {
                    window.location.reload()
                  });
                }else{
                  bootbox.alert(`${res.msg}`);
                }
              },
            })
              // .done(function (res) {})
          }
        },
      });
    }
  }
  dtButtons.push(deleteButton)

  $.extend(true, $.fn.dataTable.defaults, {
    order: [[1, 'asc']],
    pageLength: 5,
  });
  $('#dataTable:not(.ajaxTable)').DataTable({ 
    buttons: dtButtons,
    "lengthMenu": [[5, 10, 25, 50, 100, -1], [5, 10, 25, 50, 100, "All"]],
  })
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {

    $($.fn.dataTable.tables(true)).DataTable()
      .columns.adjust();
  });
});



// ######################################### my custom table 
$('.icheck-primary').find("input:checkbox[name='chk_record']").click(function(){
  // $(this).parent().parent().parent().toggleClass('bg-primary','');
  // alternative way
  if($(this).prop("checked") == true){
    $(this).parent().parent().parent().addClass('bg-primary');
  }else{
    $(this).parent().parent().parent().removeClass('bg-primary');
  }
})