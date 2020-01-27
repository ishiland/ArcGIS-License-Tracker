$(document).ready(function () {

    // Data Tables
    var usertable = $('#user-table').DataTable({
        "pageLength": 25,
        responsive: true,
        "order": [[1, "desc"]],
        dom: 'lBfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    });

    $('#user-table tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        }
        else {
            usertable.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
        window.location = $(this).data("href");
    });

    var wstable = $('#ws-table').DataTable({
        "pageLength": 25,
        responsive: true,
        "order": [[1, "desc"]],
        dom: 'lBfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    });

    $('#ws-table tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        }
        else {
            wstable.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
        window.location = $(this).data("href");
    });

    $('#server-history').DataTable({
        "pageLength": 25,
        responsive: true,
        "order": [[0, "desc"]],
        dom: 'lBfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    });

    $('#product-users').DataTable({
        "pageLength": 25,
        responsive: true,
        "order": [[0, "desc"]],
        dom: 'lBfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    });

    $('#user-products').DataTable({
        "pageLength": 25,
        responsive: true,
        "order": [[0, "desc"]],
        dom: 'lBfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    });

    $('#ws-products').DataTable({
        "pageLength": 25,
        responsive: true,
        "order": [[0, "desc"]],
        dom: 'lBfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    });

    $('#server-users-table').DataTable({
        "pageLength": 7,
        responsive: true,
        "order": [[0, "desc"]],
        dom: 'lBfrtip',
        buttons: [
            'copyHtml5',
            'excelHtml5',
            'csvHtml5',
            'pdfHtml5'
        ]
    });

    //Sortable tables
    $("#user-workstation").stupidtable();
    $("#user-server").stupidtable();
    $("#ws-workstation").stupidtable();
    $("#ws-server").stupidtable();

            $(".request-btn").on("click", function(){
        console.log(this)
    })


});




