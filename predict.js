$('#uploadForm').submit(function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    $.ajax({
        type: 'POST',
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            $('#result').text('Predicted emotion: ' + response.prediction);
        },
        error: function() {
            alert('Failed to predict emotion.');
        }
    });
});