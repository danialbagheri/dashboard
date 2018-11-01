from __future__ import division

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
import requests
import pprint
from django.http import Http404

from operator import itemgetter

import datetime
from dateutil.parser import parse


# Create your views here.
def chooseBrand(request):
	context = {}
	return render(request, "reviews/choosebrand.html", context=context)


def showReviews(request):
	NUM_REVIEWS_TO_SHOW = 10

	# get product, brand, sort/filter and page number from query string
	product = request.GET.get('product')
	if product == None:
		product = ""
	brand = request.GET.get('brand')
	if brand == None:
		brand = ""
	sort_on = request.GET.get('sort')
	page_num = request.GET.get('page')
	if page_num == None:
		page_num = 1
	# do api request to get reviews with filters

	# response = requests.get("https://api.lincocare.co.uk/reviews/?brand=%s&product=%s" % (brand, product))
	# response = requests.get("http://localhost:5000/reviews/?brand=%s&product=%s" % (brand, product))
	response = requests.get("https://api.lincocare.co.uk/reviews/?brand=%s&product=%s" % (brand, product))
	reviews = json.loads(response.text)
	# pprint.pprint(reviews)
	

	# sort reviews depending on sort query string
	reviews_to_sort = []
	for review in reviews:
		reviews_to_sort.append(reviews[review])

	# reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['name'].lower())
	if sort_on == "unpublished":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['approved'])
	elif sort_on == "published":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['approved'], reverse=True)
	elif sort_on == "recent":
		# sort on date
		# date string cheat sheet: http://strftime.org/
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: datetime.datetime.strptime( k['date_added'], "%a, %d %b %Y %X %Z" ), reverse=True)
	elif sort_on == "rating":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['score'], reverse=True)
	elif sort_on == "helpful":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['upvotes'] - k['downvotes'], reverse=True)
	else:
		# default sort by date
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: datetime.datetime.strptime( k['date_added'], "%a, %d %b %Y %X %Z" ), reverse=True)

	
	# slice to paginate
	# slice all_blogposts to get blogposts_to_show. 
	
	start_slice = page_num * NUM_REVIEWS_TO_SHOW 
	end_slice = start_slice + NUM_REVIEWS_TO_SHOW
	reviews_to_show = reviews_sorted[start_slice:end_slice]
	
	pprint.pprint(reviews_to_show)

	if len(reviews_to_show) <= 0: 
		raise Http404("No reviews to show.")


	# Make pagination numbers for the bottom of the page

	# pass reviews through to context
	



	# # Check whether there would be any more blog posts to show on the next page, and from this decide whether or not to show the NEXT PAGE button
	# start_slice += NUM_REVIEWS_TO_SHOW
	# end_slice += NUM_REVIEWS_TO_SHOW
	# next_pages_blogposts = all_blogposts[start_slice:end_slice]
	# if next_pages_blogposts.count() > 0:
	# 	show_next_page = True
	# else:
	# 	show_next_page = False

	# page_num += 1
	# next_page_num = page_num + 1
	# prev_page_num = page_num - 1

	# # Decide whether to show the PREV PAGE  button or not
	# if prev_page_num > 0:
	# 	show_prev_page = True
	# else:
	# 	show_prev_page = False


	context = { "reviews_to_show": reviews_to_show, }
	return render(request, "reviews/showreviews.html", context=context)

def reviewStats(request):
	# capture what brand we're looking at from url

	# get product filter from query string
	product = request.GET.get('product')
	if product == None:
		product = ""
	brand = request.GET.get('brand')
	if brand == None:
		brand = ""
	# do api request to get reviews with filters

	response = requests.get("https://api.lincocare.co.uk/reviews/?brand=%s&product=%s" % (brand, product))
	# response = requests.get("http://localhost:5000/reviews/?brand=%s&product=%s" % (brand, product))
	reviews = json.loads(response.text)

	# process reviews to get 
	# 	- num reviews
	#	- percentages of each stars
	# 	- num of each stars
	num_reviews = len(reviews)

	cumulative_scores = 0
	
	scores_count = [0,0,0,0,0]
	for x,y in reviews.items():
		# Count of 1, 2, 3, 4 and 5 stars respectively within reviews
		scores_count[y["score"]-1] += 1
		# Add all scores for using later to work out general score average
		cumulative_scores += y["score"]	
	
	scores_percentages = [ (x/num_reviews)*100 for x in scores_count ]
	
	overall_average = cumulative_scores/num_reviews

	context = {
		"num_reviews": num_reviews,
		"scores_count": scores_count,
		"scores_percentages": scores_percentages,
		"overall_average": overall_average,
	}
	
	return render(request, "reviews/stats.html", context=context)










