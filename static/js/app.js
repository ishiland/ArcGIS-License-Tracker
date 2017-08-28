$(document).ready(function () {
    var serverTabs = $("#products-available").children('.tab-section');
    var extensions = false;
    serverTabs.each(function (i) {
        if (location.pathname.substring(1) === 'products') {
            extensions = true
        }
        var serverDiv = serverTabs[i];
        $.ajax({
            type: 'GET',
            // async: false,
            data: {'servername': serverDiv.id, 'ext': extensions},
            contentType: 'application/json;charset=UTF-8',
            url: '_data/server/availability'
        }).done(function (data) {
            $('#' + serverDiv.id + ' > .loader').hide();
            console.log(data);
            if (data.core && data.core.length > 0) {
                var coreHtml = '<div class="overflow-auto"><table class="modifier-class product-table"><thead></th><th>Product Name</th><th>Available</th><th>Total</th></tr></thead><tbody>';
                data.core.forEach(function (element) {
                    var href = "<a href='#'><span class='icon-ui-plus-circled icon-ui-green expand-row-button' data-server=" + serverDiv.id + " data-product = " + element[0] + "></span></a>" +
                        "<a href = 'products/" + serverDiv.id + "/" + element[0] + "'>" + element[0].replace('-', ' ') + "</a>";
                    if (element[2] - element[1] === 0) {
                        coreHtml += '<tr class = "no-licenses"><td>' + href + '</td><td>' + (element[2] - element[1]) + '</td><td>' + element[2] + '</td></tr>'
                    }
                    else {
                        coreHtml += '<tr><td>' + href + '</td><td>' + (element[2] - element[1]) + '</td><td>' + element[2] + '</td></tr>'
                    }
                    coreHtml += '<tr><td colspan="3" style="display:none;" class="hidden-td"><div id =' + serverDiv.id + '-' + element[0] + ' class="loading-div"><img src="/static/images/loader.gif"></div></td></tr>';
                });
                coreHtml += '</tbody></table></div>';
                $('#' + serverDiv.id).find('.core-products').append(coreHtml);
            }
            else{
                var coreHtml = "<div class='text-centered-bold'>Unable to retrieve core license data.</div>";
                $('#' + serverDiv.id).find('.core-products').append(coreHtml);
            }
            if (data.ext && data.ext.length > 0) {
                var extHtml = '<div class="overflow-auto"><table class="modifier-class product-table"><thead></th><th>Product Name</th><th>Available</th><th>Total</th></tr></thead><tbody>';
                data.ext.forEach(function (element) {
                    var href = "<a href='#'><span class='icon-ui-plus-circled icon-ui-green expand-row-button' data-server=" + serverDiv.id + " data-product = " + element[0] + "></span></a>" +
                        "<a href = 'products/" + serverDiv.id + "/" + element[0] + "'>" + element[0].replace('-', ' ') + "</a>";
                    extHtml += '<tr><td>' + href + '</td><td>' + (element[2] - element[1]) + '</td><td>' + element[2] + '</td></tr>' +
                        '<tr><td colspan="3" style="display:none;" class="hidden-td"><div id =' + serverDiv.id + '-' + element[0] + ' class="loading-div"><img src="/static/images/loader.gif"></div></td></tr>';
                });
                extHtml += '</tbody></table></div>';
                $('#' + serverDiv.id).find('.ext-products').append(extHtml);
            }
            else{
                var extHtml = "<div class='text-centered-bold'>Unable to retrieve extension license data.</div>";
                $('#' + serverDiv.id).find('.ext-products').append(extHtml);}
            return false;
        });
    });

    // Data Tables
    var usertable = $('#user-table').DataTable({
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
        "order": [[0, "desc"]],
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

    //Sortable tables
    $("#user-workstation").stupidtable();
    $("#user-server").stupidtable();
    $("#ws-workstation").stupidtable();
    $("#ws-server").stupidtable();

});

//product availability
$(document).on('click', '.expand-row-button', function (e) {
    e.stopPropagation();
    var data = e.target.dataset;
    var div = $(this).closest('tr').next('tr').find('td');
    div.toggle(500);
    $(this).toggleClass("icon-ui-plus-circled icon-ui-green expand-row-button icon-ui-minus-circled icon-ui-red expand-row-button");
    $.ajax({
        type: 'GET',
        data: {'servername': data.server, 'product': data.product},
        contentType: 'application/json;charset=UTF-8',
        url: '_data/product/availability'
    }).done(function (d) {
        if (d.length) {
            var row = $(div).closest('tr').prev();
            var avail = row.children().eq(1).html();
            var total = row.children().eq(2).html();
            if (total - avail !== d.length) {
                row.children().eq(1).html(total - d.length).effect("highlight", {}, 1000);
            }
            if (total - avail !== 0) {
                row.css('background-color', "none")
            }
            var id = "table-" + data.server + "-" + data.product;
            var html = '<table class="modifier-class table-minimum" id=' + id + '><thead><th data-sort="string">Active Users</th><th data-sort="string">Computer ID</th><th>Current Session (min.)</th></thead><tbody>';
            d.forEach(function (element) {
                html += '<tr><td><a href="users/' + element[0] + '">' + element[0] + '</a></td><td><a href="workstations/' + element[1] + '">' + element[1] + '</a></td><td>' + element[2] + '</td>';
            });
            html += '</tbody></table>';
        }
        else {
            html = '<div class="text-centered-bold"><span class="icon-ui-check-mark icon-ui-green font-size-1">All Licenses Available</span></div>'
        }
        div.html(html);
        return false;
    });
    return false;
});