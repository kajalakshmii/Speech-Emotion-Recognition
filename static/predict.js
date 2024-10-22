$(document).ready(function() {
    $('#uploadForm').submit(function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        
        // Optional: Show a loading indicator
        $('#result').text('Processing...');

        $.ajax({
            type: 'POST',
            url: '', // Ensure this URL points to your Django view
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Accessing the correct response key
                $('#result').text('Predicted emotion: ' + response.predicted_emotion);
            },
            error: function() {
                alert('Failed to predict emotion.');
            }
        });
    });
});
