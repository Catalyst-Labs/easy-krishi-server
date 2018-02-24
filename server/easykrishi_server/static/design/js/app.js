$(function() {
  $(".navbar-expand-toggle").click(function() {
    $(".app-container").toggleClass("expanded");
    return $(".navbar-expand-toggle").toggleClass("fa-rotate-90");
  });
  return $(".navbar-right-expand-toggle").click(function() {
    $(".navbar-right").toggleClass("expanded");
    return $(".navbar-right-expand-toggle").toggleClass("fa-rotate-90");
  });
});
$(function() {
  return $(".card table.table").addClass('datatable');
});

$(function() {
  return $(".grpLst table.table thead tr").addClass('countable');
});
$(function() {
  return $(".grpMemb table.table thead tr").addClass('countable1');
});
$(function() {
  return $(".usrSellLst table.table thead tr").addClass('countable');
});
$(function() {
  return $(".usrOrdrLst table.table thead tr").addClass('countable');
});
$(function() {
  return $('select').select2();
});

$(function() {
  return $('.toggle-checkbox').bootstrapSwitch({
    size: "small"
  });
});

$(function() {
  return $('.match-height').matchHeight();
});

$(function() {
  var table = $('.datatable').DataTable( {
   orderCellsTop: true,
   "scrollX": true
} );
 
$(".dataTables_scrollHead .table thead tr").clone().appendTo($(".dataTables_scrollHead .table thead")) ;

  $('.dataTables_scrollHead .table thead tr:nth-child(2) th').each( function () {
       var title = $('.dataTables_scrollHead .table thead tr:nth-child(1) th').eq( $(this).index() ).text();
       $(this).removeAttr('class');
       $(this).html( '<input type="text" style="font-weight:normal;" placeholder="'+title.trim()+'" />' );
   } );
   $(".dataTables_scrollHead .table thead input").on( 'keyup change', function () {
       table
           .column( $(this).parent().index()+':visible' )
           .search( this.value )
           .draw();
   } );

    

 
});
$(function() {
  return $(".side-menu .nav .dropdown").on('show.bs.collapse', function() {
    return $(".side-menu .nav .dropdown .collapse").collapse('hide');
  });
});

