$(document).ready(function() {
    $('#uploadForm').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                const sentiment = response.sentiment;
                const plotFilename = response.plot_filename;
                $('#result').html(`
                    <h3>Sentiment Scores</h3>
                    <p>Compound: ${sentiment.compound}</p>
                    <p>Negative: ${sentiment.neg}</p>
                    <p>Neutral: ${sentiment.neu}</p>
                    <p>Positive: ${sentiment.pos}</p>
                    <img src="/uploads/${plotFilename}" alt="Sentiment Analysis Graph" class="img-fluid mt-3">
                `);
            }
        });
    });
});
