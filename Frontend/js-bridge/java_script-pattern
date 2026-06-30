 <script>
        console.log("Javascript was connected")
        document.getElementById('book_button').addEventListener('click',function() {
        let userNickname = document.getElementById('nickname').value;
        let userEmail = document.getElementById('email').value;
        let userPhone = document.getElementById('phone_number').value;
        let compId = document.getElementById('computer_select').value;
        let hours = document.getElementById('hours_input').value;
        let services = document.getElementById('services_select').value;
        let rawDateTime = document.getElementById('arrival_time').value;
        if (rawDateTime) {
        let parts = rawDateTime.split('T');
        let datePart = parts[0];
        let timePart = parts[1];

        let dateSplitParts = datePart.split('-')
        let year = dateSplitParts[0];
        let month = dateSplitParts[1];
        let day = dateSplitParts[2];
        var formattedDateTime = `${day}.${month} ${timePart}`;
        } else {
        var formattedDateTime = '';
        }

        let bookingData = {
            nickname: userNickname,
            email: userEmail,
            phone_number: userPhone,
            computer_id: Number(compId),
            gaming_hours: Number(hours),
            additional_services: services === 'True',
            arrival_time: formattedDateTime
        };
        console.log('given nickname:',userNickname);
        console.log('given email:',userEmail);
        console.log('given number:',userPhone);
        console.log('given arrival:',formattedDateTime);
        console.log('here is the main data:');
        console.log(bookingData);


    fetch('http://127.0.0.1:8080', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookingData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Ответ от FastAPI:', data);
        alert('Бронирование успешно создано! 🚀');
    })
    .catch(error => {
        console.error('Ошибка отправки:', error);
        alert('Косяк при отправке, проверь консоль!');
    });

});
    </script>
