from django.contrib import admin

from shops.models import Shop, Food, Record, Fooditem

class FoodInline(admin.TabularInline):
    model = Food
    extra = 3
class ShopAdmin(admin.ModelAdmin):
    list_display=['sid','name','address','teleph','owner']
    inlines = (FoodInline,)

class FoodAdmin(admin.ModelAdmin):
    list_display=['name', 'price','shop']

class FooditemInline(admin.TabularInline):
    model = Fooditem
    extra = 3
class RecordAdmin(admin.ModelAdmin):
    list_display=['buyer', 'shop', 'time', 'status']
    inlines = (FooditemInline,)

class FooditemAdmin(admin.ModelAdmin):
    list_display=['name', 'price', 'record']

admin.site.register(Shop, ShopAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Fooditem, FooditemAdmin)