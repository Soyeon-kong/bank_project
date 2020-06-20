from django.contrib import admin
from django.urls import path, include

import stock
from deposit import views
import deposit.urls
from django.conf import settings
from django.conf.urls.static import static
import board
import member
from board import urls
from member import urls
from stock import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.test),
    path('deposit/',include(deposit.urls),name='deposit'),
    path('member/', include(member.urls)),
    path('board/',include(board.urls)),
    path('stock/',include(stock.urls))
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
