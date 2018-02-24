$('.navScroll').slimscroll({
    height: 'auto',
    size: '6px',
    color: '#4671A3',
});


$(".nav-menu").click(function() {
    $(".navbar-fixed-left").toggleClass("nav-open");
    $(".nav-menu").toggleClass("nav-menu-open");
});


$('.editMbtn').click(function() {
    $('#editMTitle').focus();
});
$('.editMbtn1').click(function() {
    $('#editMTitle1').focus();
});
$('.editMbtn2').click(function() {
    $('#editMTitle2').focus();
});

$(function() {
    $('#datepicker,#datepicker1,#datepicker2,#datepicker3,#datepicker4,#datepicker5,#datepicker6,#datepicker7').datetimepicker({
        //        viewMode: 'years',
        format: 'DD/MM/YYYY'
    });
    $('#timepicker,#timepicker1,#timepicker2,#timepicker3,#timepicker4,#timepicker5,#timepicker6,#timepicker7').datetimepicker({
        format: 'h:mm a'
    });
});
if ($('#editMTitle').val() == '1') {
    $('#editMTitle').removeClass('text-warning').addClass('text-success');
} else {
    $('#editMTitle').removeClass('text-success').addClass('text-warning');
}
if ($('#editMTitle1').val() == '1') {
    $('#editMTitle1').removeClass('text-warning').addClass('text-success');
} else {
    $('#editMTitle1').removeClass('text-success').addClass('text-warning');
}
if ($('#editMTitle2').val() == '1') {
    $('#editMTitle2').removeClass('text-warning').addClass('text-success');
} else {
    $('#editMTitle2').removeClass('text-success').addClass('text-warning');
}
$("#editMTitle,#editMTitle1,#editMTitle2").change(function() {
    if ($(this).val() == '1') {
        $(this).removeClass('text-warning').addClass('text-success');
    } else {
        $(this).removeClass('text-success').addClass('text-warning');
    }
});


// feb 17
function meetingOnload(){ 
    $('#cloneAlert').hide();
    $('.cloneChooser').hide();
}

// feb 17 ends here
$('#cloneAlert').hide();
$('#cloneSel,#cloneSel1,#cloneSel2,#cloneSel3,#cloneSel4,#cloneSelG,#cloneSelG1,#cloneSelG2,#cloneSelG3,#cloneSelG4').hide();
$('#clone').click(function() {
    $('#cloneAlert').show();
    $('#cloneSel,#cloneSel1,#cloneSel2,#cloneSel3,#cloneSel4,#cloneSelG,#cloneSelG1,#cloneSelG2,#cloneSelG3,#cloneSelG4').show();
    $('#cloneMtng,#cloneMtng1,#cloneMtng2,#cloneMtng3,#cloneGMtng,#cloneGMtng1,#cloneGMtng2,#cloneGMtng3').click(function() {
        location.href = 'meetingEdit.html';
    })
});

function cloneMtng(){
    location.href = 'meetingEdit.html';
}
$('.editHlpText').focusout(function() {
    $(this).addClass('hlpTxt');
    $('.btn-toolbar.hlpBtns').hide();
});
$('.btn-toolbar.hlpBtns').hide();
$('.editHlpBtn').click(function() {
    $('.btn-toolbar.hlpBtns').show();
    $('.editHlpText').focus().removeClass('hlpTxt');
});
/*// MOM
$('#momTblAppr,#momTblAppr1,#momTblAppr2').hide();
$('.attendBtn').click(function() {
    $('#momTblAppr,#momTblAppr1,#momTblAppr2').show();
});
$('#momTblAppr3,#momTblAppr4,#momTblAppr5').hide();
$('.attendBtn1').click(function() {
    $('#momTblAppr3,#momTblAppr4,#momTblAppr5').show();
});*/



/* Calandar Dashboard */

// upcoming table 09-02-16
// $('#FullupcomTable').hide();
// $('#upcomTableLess').hide();
// $('#upcomTableMOre').click(function() {
//     $('#fiveRowupcomTable').hide();
//     $('#FullupcomTable').show();
//     $('#upcomTableMOre').hide();
//     $('#upcomTableLess').show();

// });
// $('#upcomTableLess').click(function() {
//     $('#fiveRowupcomTable').show();
//     $('#FullupcomTable').hide();
//     $('#upcomTableMOre').show();
//     $('#upcomTableLess').hide();
// });
// upcoming table 09-02-16 ends here

// assign co-ordinator 10-02-16

function hideTabeClm() {
    var elems = document.getElementsByClassName("hideClm");
    for (var i = 0; i < elems.length; i++)
        elems[i].style.display = " none";
    var elems = document.getElementsByClassName("showAssgn");
    for (var i = 0; i < elems.length; i++)
        elems[i].style.display = "none";
    
}
function hideFirstClm(){
    var elems = document.getElementsByClassName("hideClm");
    for(var i = 0; i < elems.length; i++)
    elems[i].style.display = "";
    var elems = document.getElementsByClassName("showClose");
    for (var i = 0; i < elems.length; i++)
        elems[i].style.display = "none";
    var elems = document.getElementsByClassName("showAssgn");
    for (var i = 0; i < elems.length; i++)
        elems[i].style.display = " ";
    
}
function addTxtBox(){
    var $ctrl = $('<input/>').attr({ type: 'email', name:'chk',placeholder:'Alternative email'}).addClass("alterNativeEmTxt form-control");
    $("#CheckBoxHolder").append($ctrl);
}
function addPhone(){
    var $ctrl = $('<input/>').attr({ type: 'number', name:'chk',placeholder:'Alternative phone number'}).addClass("alterNativeEmTxt form-control");
    $("#phoneholder").append($ctrl);
}
function addAddress(){
    var textBox = document.createElement("textarea");
    textBox.rows="10";
    textBox.cols="30";
    textBox.className += "alterNativeEmTxt form-control";
    document.getElementById("AddressHolder").appendChild(textBox);
    
    
}
// assign co-ordinator 10-02-16 ends here
