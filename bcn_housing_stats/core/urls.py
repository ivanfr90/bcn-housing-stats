from django.urls import path

from .apis import (
    ResourceListAPI,
    ResourceAPI,
    ResourceDataAPI)
from .views import (
    home_view,
    dashboard_view
)

app_name = "core"
urlpatterns = [
    path("", view=home_view, name="home"),
    path("dashboard", view=dashboard_view, name="dashboard")
]

# api endpoints
apipatterns = [
    path("resource/<int:pk>/", view=ResourceAPI.as_view(), name="get_resource"),
    path("resources/", view=ResourceListAPI.as_view(), name="get_resources"),
    path("resource-data/<int:resource_type_pk>/", view=ResourceDataAPI.as_view(), name="get_resource_data"),
]

urlpatterns += apipatterns
# Devolver la información del chart
# /charts/

# filtro por año
# /charts/TYPE_CHART&year=2018

# todos los años de ese chart
# /charts/TYPE_CHART
