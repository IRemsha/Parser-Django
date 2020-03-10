from django.db.models import Model, CharField, IntegerField, FloatField, BooleanField, ForeignKey, CASCADE, DO_NOTHING, ManyToManyField


class ObjectType(Model):
    name = CharField(max_length=45, unique=True)


class City(Model):
    name = CharField(max_length=250, unique=True)


class Room(Model):
    name = IntegerField(unique=True)


class Floor(Model):
    name = CharField(max_length=15, unique=True)


class Material(Model):
    name = CharField(max_length=40, unique=True)


class AdType(Model):
    name = CharField(max_length=45, unique=True)


class ObjectOldType(Model):
    name = CharField(max_length=40, unique=True)

class Site(Model):
    name = CharField(max_length=40)

class Ad(Model):
    img = CharField(max_length=350, default=None, null=True)
    price = IntegerField(default=0)
    city = ForeignKey(City, on_delete=DO_NOTHING, default=None, null=True)
    object_type = ForeignKey(ObjectType, on_delete=DO_NOTHING, default=None, null=True)
    room = ForeignKey(Room, on_delete=DO_NOTHING, default=1)
    floor = ForeignKey(Floor, on_delete=DO_NOTHING, default=1)
    square_all = IntegerField(default=0)
    square_kitchen = IntegerField(default=0)
    square_live = IntegerField(default=0)
    material = ForeignKey(Material, on_delete=DO_NOTHING, default=1)
    ad_type = ForeignKey(AdType, on_delete=DO_NOTHING, default=1)
    url = CharField(max_length=400, unique=True, default=None, null=True)
    last_seen = IntegerField(default=0)
    object_old_type = ForeignKey(ObjectOldType, on_delete=DO_NOTHING, default=None, null=True)
    site = ForeignKey(Site, on_delete=DO_NOTHING, default=None, null=True)