import scrapy
import re
from scrapy.spiders import CrawlSpider
# Username: englishprofile
# Password: vocabulary

urls = ['http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/A/1001497', 
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/B/1005691',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/C/1185916',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/D/1016799',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/E/1021237',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/F/3265887',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/G/3352247',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/H/1032335',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/I/1087281',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/J/1038422',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/K/2001716',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/L/1039771',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/M/1042506',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/N/1046648',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/O/1048340',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/P/1050324',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/Q/3394355',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/R/1057115',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/S/1060918',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/T/1070752',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/U/2001218',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/V/3408153',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/W/1077528',
				'http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/X/3408466',				
				]



# EPD = English Profile Dataset
class EPDSpider(CrawlSpider):
	name = "epd_spider"
	http_user = 'englishprofile'
	http_pass = 'vocabulary'
	handle_httpstatus_list = [401]
	start_urls = ['http://vocabulary.englishprofile.org/dictionary/word-list/uk/a1_c2/A/1001497']
	i = 0	
	# parse text
	def parse(self, response):
		
		# convert from byteobj to string
		text = response.body.decode("utf-8")

		# # write the html code
		# with open("full.txt", 'w') as file:
		# 	file.write(text)
		# 	file.close()

		# use regex to find the words definition and difficulty
		regstring = '<span class="base">([a-zA-Z]+).+<span class="freq-([ABC]\d)'
		regstring1 = '<span class="base">([a-zA-Z]+).+<span class="gw">([a-zA-Z\s]+).+<span class="freq-([ABC]\d)'
		result = re.findall(regstring, text)

		# write a csv
		with open("results.csv", 'a') as file:
			
			# label columns
			# file.write('word, definition, difficulty')
			file.write('word, difficulty')
			file.write('\n')
			
			# write each row
			for row in result:
				file.write(", ".join(row))
				file.write('\n')

			# close file
			file.close()

		next_page = response.css('a[title="Next"]::attr(href)').extract_first()

		if next_page is None:
			self.i+=1
			if len(urls) > self.i:
				yield scrapy.Request(urls[self.i], callback=self.parse)
		else:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)