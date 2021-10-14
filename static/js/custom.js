
$(document).ready(function() {
    setTimeout(function() {
        $(".alert-dismissible").hide();
    }, 3000);
});



$(document).ready(function() {
    $('.select2').select2();
});


$('.delete-btn').click(function(e) {
    e.preventDefault();
        // url = $(this).attr('data-url');
        // url = $(this).data('url');
    let form = $(this).parent().find('form');
    bootbox.confirm({
        title: "Delete Record?",
        message: "Are you sure you want to delete this data?",
        buttons: {
            cancel: {
                label: '<i class="fa fa-times"></i> Cancel'
            },
            confirm: {
                label: '<i class="fa fa-check"></i> Confirm'
            }
        },
        callback: function (result) {
            if(result){
            form.submit();
            }
        }
    });
})





var toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
var currentTheme = localStorage.getItem('theme');
var mainHeader = document.querySelector('.main-header');

if (currentTheme) {
    if (currentTheme === 'light') {
        if (document.body.classList.contains('dark-mode')) {
        document.body.classList.remove("dark-mode");
        }
        if (mainHeader.classList.contains('navbar-dark')) {
        mainHeader.classList.remove('navbar-dark');
        mainHeader.classList.add('navbar-light');
        }
        
        toggleSwitch.checked = false;
    }
}

function switchTheme(e) {
    if (e.target.checked) {
        if (document.body.classList.contains('dark-mode')) {
        document.body.classList.remove("dark-mode");
        }
        if (mainHeader.classList.contains('navbar-dark')) {
        mainHeader.classList.remove('navbar-dark');
        mainHeader.classList.add('navbar-light');
        }
        localStorage.setItem('theme', 'light');
    } else {
        if (!document.body.classList.contains('dark-mode')) {
        document.body.classList.add("dark-mode");
        }
        if (!mainHeader.classList.contains('navbar-dark')) {
        mainHeader.classList.add('navbar-dark');
        mainHeader.classList.remove('navbar-light');
        }
        localStorage.setItem('theme', 'dark');
    }
}

toggleSwitch.addEventListener('change', switchTheme, false);


