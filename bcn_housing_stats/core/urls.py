from django.urls import path

from .apis import (ResourceListAPI, ResourceAPI, ResourceDataAPI, ResourceTypeAPI, ResourceTypeListAPI)
from .views import (
    dashboard_view,
    datatables_view)

app_name = "core"

# urls
urlpatterns = [
    path("", view=dashboard_view, name="dashboard"),
    path("datatables", view=datatables_view, name="datatables")
]

# api endpoints
apipatterns = [
    path("resources/<int:pk>/", view=ResourceAPI.as_view(), name="get_resource"),
    path("resources/", view=ResourceListAPI.as_view(), name="get_resources"),
    path("resources-types/<int:pk>/", view=ResourceTypeAPI.as_view(), name="get_resource_type"),
    path("resources-types/", view=ResourceTypeListAPI.as_view(), name="get_resources_types"),
    path("resource-data/<int:resource_type_pk>/", view=ResourceDataAPI.as_view(), name="get_resource_data"),
]

urlpatterns += apipatterns
