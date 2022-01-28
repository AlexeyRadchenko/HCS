<template>
<div class="wrapper">
    <div class="container">
  <router-link to="/management_accounts" style="display: inline-block;text-decoration:none; color: rgb(250, 250, 250)">        
  <div class="items">
    <div class="icon-wrapper">
      <font-awesome-icon :icon="['fas', 'address-card']" size="7x" />
    </div>
    <div class="project-name">
      <p>СПРАВОЧНИК</p>
    </div>
  </div>
  </router-link>  
  <div class="items">
    <div class="icon-wrapper">
      <font-awesome-icon :icon="['fas', 'money-check']" size="7x" />
    </div>
    <div class="project-name">
      <p>ЗАДОЛЖЕННОCТЬ ПО И/Л</p>
    </div>
  </div>
  <div class="items">
    <div class="icon-wrapper">
      <i class="fa fa-th-large"></i>
    </div>
    <div class="project-name">
      <p>COLLECTIONS</p>
    </div>
  </div>  
</div>
</div>
</template>

<style lang="scss" scoped>
//    $pri: #FD2549;
$sec: #E5E6F1;

body {
  box-sizing: border-box;
  font-family: 'Raleway', sans-serif;
}
.wrapper{
background: #50a3a2;
background: -webkit-linear-gradient(top left, #50a3a2 0%, #53e3a6 100%);
background: -moz-linear-gradient(top left, #50a3a2 0%, #53e3a6 100%);
background: -o-linear-gradient(top left, #50a3a2 0%, #53e3a6 100%);
background: linear-gradient(to bottom right, #50a3a2 0%, #53e3a6 100%);
	
	position: absolute;
	/*top: 50%;*/
	left: 0;
	width: 100%;
  height: 100%;
	/*height: 400px;
	margin-top: -200px;*/
	overflow: hidden;
	
	&.form-success{
		.container{
			h1{
				transform: translateY(85px);
			}
		}
	}
}

.container {
  width: 800px;
  height: 250px;
  
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  margin: auto;
  box-sizing: border-box;
  
  display: grid;
  grid-template-columns: repeat( auto-fit, minmax(250px, 1fr) );
  grid-template-rows: 1fr;
  grid-gap: 15px;
}

.items {
  border-radius: 5px;
  display: grid;
  grid-template-rows: 2fr 1fr;
  grid-gap: 10px;
  cursor: pointer;
  border: 3px dotted black;
  transition: all 0.6s;
}


.icon-wrapper, .project-name {
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper i {
  font-size: 100px;
  color: $sec;
  transform: translateY(0px);
  transition: all 0.6s;
}

.icon-wrapper {
  align-self: end;  
}

.project-name {
  align-self: start;
}
.project-name p {
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 2px;
  color: $sec;  
  transform: translateY(0px);
  transition: all 0.5s;
}

.items:hover {
  border: 3px solid $sec;
  
  & .project-name p {
    transform: translateY(-10px);
  }
  & .icon-wrapper i {
    transform: translateY(5px);
  }
}

nav li:hover,
 nav li.router-link-active,
 nav li.router-link-exact-active {
   background-color: indianred;
   cursor: pointer;
   text-decoration: none;
 }
</style>