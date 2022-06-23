from django.urls import path, include
from . import views
 
urlpatterns = [
    path('', views.index,name="pfc"),
    path('profilage1/', views.profilage1,name="profilage1"),
    path('profilage2/', views.profilage2,name="profilage2"),
    path('profilage3/', views.profilage3,name="profilage3"),
    path('col1/',views.col1,name="col1"),
    path('col3/',views.col3,name="col3"),
    path('col4/',views.col4,name="col4"),
    path('col5/',views.col5,name="col5"),
    path('col6/',views.col6,name="col6"),
    path('col7/',views.col7,name="col7"),
    path('col8/',views.col8,name="col8"),
    path('col9/',views.col9,name="col9"),
    path('col10/',views.col10,name="col10"),
    path('stat/',views.stat,name="stat"),
    path('stat2/',views.stat2,name="stat2"),
    path('stat3/',views.stat3,name="stat3"),
    path('stat4/',views.stat4,name="stat4"),
    path('stat5/',views.stat5,name="stat5"),
    path('stat6/',views.stat6,name="stat6"),
    path('stat7/',views.stat7,name="stat7"),
    path('stat8/',views.stat8,name="stat8"),
    path('stat9/',views.stat9,name="stat9"),
    path('export1/',views.export1,name="export1"),
    path('export2/',views.export2,name="export2"),
    path('export3/',views.export3,name="export3"),
    path('statl1/',views.statl1,name="statl1"),
    path('statl2/',views.statl2,name="statl2"),
    path('statl3/',views.statl3,name="statl3"),
    path('statl4/',views.statl4,name="statl4")
]