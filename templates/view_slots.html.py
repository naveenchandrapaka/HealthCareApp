<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>View Available Appointment Slots</title>
    <!-- Add any required CSS or JS here -->
</head>
<body>
<h2>Select a Doctor and Date to View Available Slots</h2>
<form action="{{ url_for('view_slots') }}" method="post">
    {{ form.hidden_tag() }}
    <div>
        <label for="doctor_id">Doctor:</label>
        {{ form.doctor_id }}
        {% for error in form.doctor_id.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>
    <div>
        <label for="date">Date:</label>
        {{ form.date }}
        {% for error in form.date.errors %}
            <span style="color: red;">{{ error }}</span>
        {% endfor %}
    </div>
    {{ form.submit() }}
</form>

{% if available_slots %}
    <h3>Available Slots on {{ selected_date }} for Dr. {{ selected_doctor_name }}</h3>
    <!-- Assume we have an endpoint 'book_appointment' for booking -->
    <form action="{{ url_for('book_appointment') }}" method="post">
        <!-- Loop through the available slots and display them as options -->
        {% for slot in available_slots %}
            <div>
                <input type="radio" id="slot{{ loop.index }}" name="start_time" value="{{ slot.start_time }}">
                <label for="slot{{ loop.index }}">{{ slot.start_time.strftime('%I:%M %p') }}</label>
            </div>
        {% endfor %}
        <input type="hidden" name="patient_id" value="{{ patient_id }}">
        <input type="hidden" name="doctor_id" value="{{ selected_doctor_id }}">
        <input type="hidden" name="date" value="{{ selected_date }}">
        {{ form.submit() }}
    </form>
{% else %}
    <p>No slots available for the selected date. Please try a different date.</p>
{% endif %}
</body>
</html>
