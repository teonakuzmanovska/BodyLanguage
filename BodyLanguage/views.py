from django.contrib import messages
from django.shortcuts import redirect, render

# Create your views here.
from BodyLanguage.forms import UserRegistrationForm
from BodyLanguage.models import *


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def contact(request):
    return render(request, "contact.html")


def helphtml(request):
    return render(request, "help.html")


def tips(request):
    return render(request, "tips.html")


def articles(request):
    return render(request, "articles.html")


def categories(request):
    return render(request, "categories.html")


def quizzes(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            questions = Question.objects.all()
            points = 0
            category = request.POST.get("category", "")
            for q in questions:
                # the user gets +1 point for correct answer
                if q.ans == request.POST.get(q.question):
                    points += 1

            #  reinsert points if present
            if Results.objects.filter(user=request.user).filter(category=category).count():
                Results.objects.filter(user=request.user).filter(category=category).all().delete()

            result = Results(category=category, points=points, user=request.user)
            result.save()

            return redirect("progress")

        else:
            random = Question.objects.filter(category="random").all()
            body_parts = Question.objects.filter(category="body_parts").all()
            emotions = Question.objects.filter(category="emotions").all()
            contexts = Question.objects.filter(category="contexts").all()
            behaviours = Question.objects.filter(category="behaviours").all()

            context = {"random": random, "body_parts": body_parts, "emotions": emotions, "contexts": contexts, "behaviours": behaviours}
            return render(request, 'quizzes.html', context=context)

    else:
        return redirect("/login/")


def progress(request):

    if request.user.is_authenticated:

        # instances of ResultsModel for all categories
        random = Results.objects.filter(user=request.user).filter(category="random").all()
        body_parts = Results.objects.filter(user=request.user).filter(category="body_parts").all()
        emotions = Results.objects.filter(user=request.user).filter(category="emotions").all()
        contexts = Results.objects.filter(user=request.user).filter(category="contexts").all()
        behaviours = Results.objects.filter(user=request.user).filter(category="behaviours").all()

        # number of available tests
        randomCount = Question.objects.filter(category="random").count()
        body_partsCount = Question.objects.filter(category="body_parts").count()
        emotionsCount = Question.objects.filter(category="emotions").count()
        contextsCount = Question.objects.filter(category="contexts").count()
        behavioursCount = Question.objects.filter(category="behaviours").count()


        # sum of points for each test
        sumR = sumPoints(Results.objects.filter(user=request.user).filter(category="random").count(), random)
        sumBP = sumPoints(Results.objects.filter(user=request.user).filter(category="body_parts").count(), body_parts)
        sumE = sumPoints(Results.objects.filter(user=request.user).filter(category="emotions").count(), emotions)
        sumC = sumPoints(Results.objects.filter(user=request.user).filter(category="contexts").count(), contexts)
        sumB = sumPoints(Results.objects.filter(user=request.user).filter(category="behaviours").count(), behaviours)

        # calculating overal score
        score = (sumBP + sumE + sumC + sumB) * 100 / (body_partsCount + emotionsCount + contextsCount + behavioursCount) + calculatePercentage(sumR, randomCount)/10

        context = {
            "score": score,
            "random": calculatePercentage(sumR, randomCount),
            "body_parts": calculatePercentage(sumBP, body_partsCount),
            "emotions": calculatePercentage(sumE, emotionsCount),
            "context": calculatePercentage(sumC, contextsCount),
            "behaviours": calculatePercentage(sumB, behavioursCount),
        }
        return render(request, 'progress.html', context=context)
    else:
        return redirect("/login/")


def calculatePercentage(userPoints, allPoints):
    if type(userPoints) == int:
        return (userPoints / allPoints) * 100
    else:
        return 0


def sumPoints(numberOfObjects, points):
    if numberOfObjects > 0:
        sum = 0
        for point in points:
            sum += point.points
        return sum
    else:
        return 0


def body_parts(request):
    face = Gesture.objects.filter(category="face").all()
    arms = Gesture.objects.filter(category="arms").all()
    legs = Gesture.objects.filter(category="legs").all()

    context = {"face": face, "arms": arms, "legs": legs}

    return render(request, "body_parts.html", context=context)


def emotions(request):
    happiness = Gesture.objects.filter(meaning__meaning="happiness").all()
    sadness = Gesture.objects.filter(meaning__meaning="sadness").all()
    shame = Gesture.objects.filter(meaning__meaning="shame").all()
    guilt = Gesture.objects.filter(meaning__meaning="guilt").all()
    disgust = Gesture.objects.filter(meaning__meaning="disgust").all()
    anger = Gesture.objects.filter(meaning__meaning="anger").all()
    fear = Gesture.objects.filter(meaning__meaning="fear").all()

    context = {"happiness": happiness, "sadness": sadness, "shame": shame, "guilt": guilt, "disgust": disgust, "anger": anger, "fear": fear}
    return render(request, "emotions.html", context=context)


def context(request):
    return render(request, "context.html")
