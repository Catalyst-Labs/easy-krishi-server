$(document).ready(function () {

    $('.small-calendar').fullCalendar({
        defaultDate: '2016-01-12',
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: [
            {
                title: 'All Day Event',
                start: '2016-01-01'
				},
            {
                title: 'Long Event',
                start: '2016-01-07',
				},
            {
                id: 999,
                title: 'Repeating Event',
                start: '2016-01-09T16:00:00'
				},
            {
                id: 999,
                title: 'Repeating Event',
                start: '2016-01-16T16:00:00'
				},
            {
                title: 'Conference',
                start: '2016-01-11',
				},
            {
                title: 'Meeting',
                start: '2016-01-12T10:30:00',
				},
            {
                title: 'Lunch',
                start: '2016-01-12T12:00:00'
				},
            {
                title: 'Meeting',
                start: '2016-01-12T14:30:00'
				},
            {
                title: 'Happy Hour',
                start: '2016-01-12T17:30:00'
				},
            {
                title: 'Dinner',
                start: '2016-01-12T20:00:00'
				},
            {
                title: 'Birthday Party',
                start: '2016-01-13T07:00:00'
				}

			]
    });
    
    $('.normal-calendar').fullCalendar({
			header: {
				left: 'prev,next today',
				center: 'title',
				right: 'month,agendaWeek,agendaDay'
			},
			defaultDate: '2016-01-12',
			selectable: true,
			selectHelper: true,
			select: function(start, end) {
				var title = prompt('Event Title:');
				var eventData;
				if (title) {
					eventData = {
						title: title,
						start: start,
						end: end
					};
					$('.normal-calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
				}
				$('.normal-calendar').fullCalendar('unselect');
			},
			editable: true,
			eventLimit: true, // allow "more" link when too many events
			events: [
				{
					title: 'All Day Event',
					start: '2016-01-01'
				},
				{
					title: 'Long Event',
					start: '2016-01-07',
				},
				{
					id: 999,
					title: 'Repeating Event',
					start: '2016-01-09T16:00:00'
				},
				{
					id: 999,
					title: 'Repeating Event',
					start: '2016-01-16T16:00:00'
				},
				{
					title: 'Conference',
					start: '2016-02-02',
				},
				{
					title: 'Meeting',
					start: '2016-01-12T10:30:00',
				},
				{
					title: 'Lunch',
					start: '2016-01-12T12:00:00'
				},
				{
					title: 'Happy Hour',
					start: '2016-01-12T17:30:00'
				},
				{
					title: 'Dinner',
					start: '2016-01-12T20:00:00'
				},
				{
					title: 'Birthday Party',
					start: '2016-01-13T07:00:00'
				}
			]
		});


});