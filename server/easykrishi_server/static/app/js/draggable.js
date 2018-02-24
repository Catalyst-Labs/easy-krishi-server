/* draggable */
$(function () {
    $(".draggable").draggable({
        revert: false,
        helper: "clone",
        cursor: "move",
        containment: ".meetToAdenda"
    });
    $( "#headingTwo1").draggable({
            drag: function() {
                $('.draggedVal').val("Annual General Meeting");
            }
    });
    $( "#headingTwo2").draggable({
            drag: function() {
                $('.draggedVal').val("Extra-ordinary General Meeting");
            }
    });
    $( "#headingThree1").draggable({
            drag: function() {
                $('.draggedVal').val("Company's First Board Meeting");
            }
    });
    $( "#headingThree2").draggable({
            drag: function() {
                $('.draggedVal').val("Meeting in which Annual Accounts are Approved");
            }
    });
    $( "#headingThree3").draggable({
            drag: function() {
                $('.draggedVal').val("Periodic Board Meetings");
            }
    });
    $( "#headingOne1").draggable({
            drag: function() {
                $('.draggedVal').val("Audit Committee");
            }
    });
    $( "#headingOne2").draggable({
            drag: function() {
                $('.draggedVal').val("Nomination and Remuneration Committee");
            }
    });
    $("#droppable").droppable({
        drop: function (event, ui) {
            $(".showonlist").removeClass("dn");
            $(".showonlist").addClass("db");
            console.log("drop");
        }
    });
});