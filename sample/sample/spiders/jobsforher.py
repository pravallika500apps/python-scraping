import scrapy
from scrapy import Selector

class JobsforherSpider(scrapy.Spider):
    name = "jobsforher"
    allowed_domains = ["jobsforher.com"]
    start_urls = ["https://www.jobsforher.com/jobs"]

    def parse(self, response):
        print('hiii')
        jobsforher = response.xpath("//div[@class='card-body']//a[@class='text-left mb-1']").xpath('@href').getall()
        url_data = response.xpath('//*[@id="job"]/div[2]/div/div[1]/div/div[2]/a').xpath("@id").getall()
        for job in jobsforher:
            job_url = "https://www.jobsforher.com/jobs"+job
            yield scrapy.Request(url=job_url, callback=self.parse_job)
    def parse_job(self, response):
        # print("=== Job Details ===",response)
        Jobtitle = response.xpath("//div[@class='d-flex']//h1/text()").get().strip()
        Jobcompany = response.xpath("//div//h2[@class='pl-2 jd-title2-18']/text()").get().strip()
        JobArea = response.xpath("//div[@class='mb-1 jd-title3-18 d-none d-md-block']/text()").get().strip().replace("\n","").replace("\t","")

        try:
            Jobdescription = response.xpath("//div[@class='descriptionless jd-title-color']/text()").getall().strip()
        except:
            Jobdescription = response.xpath("//div[@class='descriptionless jd-title-color']/text()").getall()

        job_dict = {
            'Jobtitle': Jobtitle,
            'Jobcompany': Jobcompany,
            'JobArea': JobArea,
            'Jobdescription': Jobdescription
        }
        print(job_dict , "::::::::::::::::::::::::")
        job_details = response.xpath("//div[@class='mb-3']").getall()
        for i in job_details:
            tit = Selector(text=i)
            k = tit.xpath("//p[@class='text-12 color-9A9A9A']/text()").get().strip()
            v = tit.xpath("//p[@class='text-12 color-6F6E6E']/text()").get().strip()
            job_dict[k]=v
        print(job_dict)
        yield job_dict

