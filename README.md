<!-- TABLE OF CONTENTS -->
## Table of Contents
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#team-members">Team Members</a></li>
      </ul>
    </li>
    <li><a href='#prerequisites'>Prerequisites</a></li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#clone">Clone</a></li>
        <li><a href="#database-setup">Database Setup</a></li>
        <li><a href="#docker-setup">Docker Setup</a></li>
        <li><a href="#test-account">Test Account</a></li> 
      </ul>
    </li>
    <li><a href='#api-documentations'>API Documentations</a></li>
  </ol>

<br/>
<br/>

## About The Project

<p align="center">
    <img src="./my_app/src/assets/images/logos/large_logos/MakanBoleh_logo_long_light_large.png" >
</p>

<p align=center>
    Remember seeing that plate of succulent chicken being thrown away after the buffet ends?  Always hearing about food wastage in Singapore but never knew what to do about it? MakanBoleh seeks to resolve both conundrums with a single click and a satisfied stomach at a time.
</p>

<p align=center>
"Got food? Just share!"
</p>


### Built With

* <a href="https://html.com/"><img width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg"/></a>
* <a href="https://developer.mozilla.org/en-US/docs/Web/CSS"><img width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"/></a>
* <a href="https://www.javascript.com/"><img width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"/></a>
* <a href="https://vuejs.org/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg" width="26px"></a>
* <a href="https://getbootstrap.com"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" width="26px"></a>
* <a href="https://firebase.google.com/?gclid=CjwKCAiA68ebBhB-EiwALVC-Nu9CUOHBl_f4ytQaPMxt6hrueI-AQV3jTr1F-8u7dtfenil2eMGkNhoCH2YQAvD_BwE&gclsrc=aw.ds"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/firebase/firebase-plain.svg" width="26px"></a>
* <a href="https://www.docker.com/"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="26px"></a>

<br/>

### Team Members

| Members               | School Email     | Email                           |
| --------------------- | ---------------- | ------------------------------- |
| Tan Sheng Da                   | shengda.tan.2021 | shengdatan@gmail.com            |
| Ang Keng Boon         | kbang.2021 | kbang.2021@scis.smu.edu.sg    |
| Muhammad Faez Bin Abdul Latiff | muhammadal.2021  | faezlatiff0706@gmail.com|
| Sng Yue Wei, Rachel            | rachel.sng.2021  | rrachelsng@gmail.com    |
| Adam Tan          | adam.tan.2021  |  adamft.2021@scis.smu.edu.sg   |
| Seth Yap Zi Qi            | seth.yap.2021  | seth.yap.2021@scis.smu.edu.sg   |


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<br/>
<br/>

## Prerequisites
Please ensure your machine has the prerequisites required for MakanBoleh
* WAMP (Windows User): https://www.wampserver.com/en/
* MAMP (Mac User): https://www.mamp.info/en/mac/
* Docker Desktop: https://www.docker.com/products/docker-desktop/

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<br/>
<br/>

## Installation

### Clone
Clone the github repository to your local machine by typing in the terminal `git clone https://github.com/tan-sd/makan-boleh.git`

### Database Setup
1. Turn on WAMP/MAMP
2. Login into phpMyAdmin by typing `http://localhost/phpmyadmin/` in your browser and click the `Import` tab
3. Click `Choose file` and navigate to `makan-boleh > databases` and select the files
4. Click `Go`
5. Repeat steps till all SQL files have been imported

### Docker Setup
1. Turn on Docker Desktop
2. On the terminal, type `cd makan-boleh`
3. Then `docker compose up`
4. Once container has been built and ran, you can access MakanBoleh through `http://localhost:8080`

### Test Account
| **Username**       | **iloveesd** |
| -------------- | ------------------|
| **Password**       | **Password123**  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<br/>
<br/>

## API Documentations
* <a href='https://docs.google.com/document/d/1rcwscbMF9YDxRCl7xgJOnmwe-a4l3_Y2pBSY2JJV-xk/edit?usp=sharing'>FoodInfo API</a>
* <a href='https://docs.google.com/document/d/1SiL-nAZGWvSLyYBr0qHcx1SPB6T_fvILyldV88--p_k/edit?usp=sharing'>UserInfo API</a>
* <a href='https://docs.google.com/document/d/1JjyuweIMLZUxryOB_myYrGjy_7T0CKj6pkzmQwBIxKE/edit?usp=sharing'>ManageForum API</a>
* <a href='https://docs.google.com/document/d/19xZsvWSiL8xJQJ24d46SP0UV9PYQkdYDaqvmw0iBgIs/edit?usp=sharing'>FindFood API</a>
* <a href='https://docs.google.com/document/d/1eoJdZa1_9Lzpfskz_SwqR_2HTqOayMGp46h_-Q5Uet4/edit?usp=sharing'>ManageFood API</a>
* <a href='https://docs.google.com/document/d/18bd7cptYZtRFWiYMjcIRoYCyZaP-1_UyFL95OAGsNJs/edit?usp=sharing'>Forum API</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>