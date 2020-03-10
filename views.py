from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ad


class Result(APIView):
	def get(self, request, page, amount_per_page):
		print(page)
		result = Ad.objects.filter()
		result_clean = []
		for r in result:
			result_clean.append({
				'id': r.id,
				'price': r.price,
				'city': r.city.name,
				'square': r.square_all,
				'square_live': r.square_live,
				'square_kitchen': r.square_kitchen,
				'ad_type': r.ad_type.name,
				'floor': r.floor.name,
				'material': r.material.name,
				'room':  r.room.name,
				'object_type': r.object_type.name,
				'url': r.url,
				'object_old_type': r.object_old_type.name,
				'img': r.img,
				'site': r.site.name
			})
		return Response(result_clean)