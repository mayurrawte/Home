$(document).ready(function() {
    $('#helpform').on('submit', function(e) {
        e.preventDefault();
        var isValid = $(this).valid();
        console.log(isValid);
        if(isValid) {
            $('#nav-help').modal('hide');
            var data = $('#helpform').serializeArray();
        $.ajax({
            url : '/send-mail/',
            type: 'POST',
            data: {
                'type': 'help',
                'name': data[0].value,
                'email': data[1].value,
                'subject': 'Need Help !',
                'message': data[2].value
            },
            success: function(json) {
                $('#alert').html('<div class="alert alert-success">Message Sent Successfully ! <br /> I will get back to you soon !</div>' );
                $('#alert').modal('show');
            },
            error: function(xhr,errmsg,err) {
                $('#alert').html('<div class="alert alert-danger">Internal Error</div>' );
                $('#alert').modal('show');
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
        } else {
            alert('form is invalid');
        }

    });

    $('#hireme-form').on('submit', function(e) {
        e.preventDefault();
        var isValid = $('#hireme-form').valid();
        if(isValid) {
            var data = $('#hireme-form').serializeArray();
            $('#nav-hireme').modal('hide');
        $.ajax({
            url : '/send-mail/',
            type: 'POST',
            data: {
                'type': 'hire',
                'email': data[0].value,
                'message': data[1].value,
                'name': ''
            },
            success: function(json) {
                $('#alert').html('<div class="alert alert-success">Thanks for this ! <br /> I will get back to you soon !</div>' );
                $('#alert').modal('show');
            },
            error: function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
        } else {
            $('#alert-message').html('<div class="alert alert-danger">Invalid Form Data</div>');
            $('#alert').modal("show");
        }
    });
});