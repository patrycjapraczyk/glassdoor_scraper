from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep


class GlassdoorScrapper:
    URL = "https://www.glassdoor.com/index.htm"

    def __init__(self):
        # create a new Firefox session
        options = Options()
        #options.add_argument('headless')
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(30)
        self.driver.set_window_size(1120, 1000)

    def close_sign_up_modal(self):
        """
            closes the sign up modal appearing on Glassdoor every few minutes
        """
        try:
            self.driver.find_element_by_id('"prefix__icon-close-1"').click()
        except NoSuchElementException:
            pass

    def search_jobs(self, keyword, location='', num_jobs=10):
        keyword.replace(' ', '+')
        url = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&' \
              'typedKeyword=' + keyword +'&sc.keyword=' + keyword + '&locT=C&locId=2955165&jobType='
        self.driver.get(url)

    def get_jobs(self, keyword, location='', num_jobs=10):
        self.search_jobs(keyword, location, num_jobs)

        jobs = []
        job_elems = self.driver.find_element_by_class_name("jl")

        while len(jobs) < num_jobs:
            self.close_sign_up_modal()
            job = self.extract_job_info()
            print(str(job))
            jobs.append(job)
            sleep(5)

    def extract_job_info(self):
        company_name = self.driver.find_element_by_xpath('.//div[@class="employerName"]').text
        location = self.driver.find_element_by_xpath('.//div[@class="location"]').text
        job_title = self.driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
        job_description = self.driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text

        job = {
            'company_name': company_name,
            'location': location,
            'job_title': job_title,
            'job_description': job_description
        }

        return job


glassdoor_scrapper = GlassdoorScrapper()
glassdoor_scrapper.get_jobs('developer', num_jobs=3)
