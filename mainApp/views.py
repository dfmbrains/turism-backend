from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./mainApp/turism-kg-firebase-adminsdk-rl6la-d79b9878af.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

config = {
    "apiKey": "AIzaSyDYqaZHBeiQvPCpKDGToOjWRPiwasstC5A",
    "authDomain": "turism-kg.firebaseapp.com",
    "databaseURL": "https://turism-kg-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "turism-kg",
    "storageBucket": "turism-kg.appspot.com",
    "messagingSenderId": "619463410757",
    "appId": "1:619463410757:web:5d47b0f603db15d56d4f2c"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


@api_view(['POST'])
def book(request):
    if request.method == "POST":
        aparts = request.POST.get("aparts")
        user = request.POST.get("user")
        date_start = request.POST.get("date_start")
        date_end = request.POST.get("date_end")
        persons = request.POST.get("persons")
        if aparts is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, "message": "Укажите id апартаментов!"})
        if user is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, "message": "Укажите id пользователя!"})
        if date_start is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, "message": "Укажите дату начала брони!"})
        if date_end is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, "message": "Укажите дату конца брони!"})
        if persons is None:
            return Response({'status': status.HTTP_204_NO_CONTENT, "message": "Укажите количество человек!"})
        data = {
            "aparts_id": aparts,
            "user_id": user,
            "date_start": date_start,
            "date_end": date_end,
            "persons": persons,
        }
        if len(db.collection("bookings").where("aparts_id", "==", aparts).where("date_start", "==", date_start) \
                .where("date_end", "==", date_end).get()) != 0:
            return Response({'status': status.HTTP_406_NOT_ACCEPTABLE, 'message': "Бронь уже занята"})
        else:
            doc_ref = db.collection(u'bookings').add(data)
            data = list(db.collection('bookings').where("aparts_id", "==", aparts).where("user_id", "==", user) \
                        .where("date_start", "==", date_start) \
                        .where("date_end", "==", date_end).where("persons", "==", persons).stream())
            return Response({
                'status': status.HTTP_200_OK,
                'message': "Бронь была успешно создана.",
                'id': f"{data[0].id}"
            })

    return Response({'status': status.HTTP_406_NOT_ACCEPTABLE, 'message': "Ошибка"})
