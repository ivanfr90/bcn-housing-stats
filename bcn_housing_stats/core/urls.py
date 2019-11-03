from django.urls import path

from bcn_housing_stats.core.views import (
    home_view
)

app_name = "core"
urlpatterns = [
    path("", view=home_view, name="home")
]
