from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import geckodriver_autoinstaller


class GlassdoorScrapper:
    URL = "https://www.glassdoor.com/index.htm"

    def __init__(self):
        # create a new Firefox session
        geckodriver_autoinstaller.install()
        self.driver = webdriver.Firefox()
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
        jobs = self.driver.find_elements_by_class_name('react-job-listing')
        jobs_counter = 0
        while jobs_counter < num_jobs:
            self.close_sign_up_modal()
            job = self.extract_job_info(jobs[jobs_counter])
            print(str(job))
            jobs.append(job)
            sleep(5)
            jobs_counter += 1

    def extract_job_info(self, job):
        company_name = job.find_elements_by_class_name('css-l2wjgv')[0].text
        location = job.find_elements_by_class_name('pr-xxsm')[0].text
        job_title = job.find_elements_by_class_name('eigr9kq2')[0].text
        #job_description = self.driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
        job = {
            'company_name': company_name,
            'location': location,
            'job_title': job_title
            #'job_description': job_description
        }
        return job


glassdoor_scrapper = GlassdoorScrapper()
glassdoor_scrapper.get_jobs('developer', num_jobs=3)
