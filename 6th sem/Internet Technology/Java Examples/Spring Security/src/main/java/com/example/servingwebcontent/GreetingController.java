package com.example.servingwebcontent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@Controller @CrossOrigin
public class GreetingController {
	
	
	@Autowired
	PersonRepository repository;
	
	@GetMapping("/greeting/{str}")
	//public String greeting(@RequestParam(name="name", required=false, defaultValue="World") String name, Model model) {
	public String greeting(@PathVariable("str") String name, Model model) {
		
		model.addAttribute("name", name);
		
		return "greeting";
	}

	@PostMapping("/greeting1")
	public String greeting(@RequestParam(name="fname",required=true) String fname, @RequestParam(name="lname", required=true) String lname, Model model) {
	//public String greeting(@PathVariable("str") String name, Model model) {
		
		//model.addAttribute("fname", fname);
		//model.addAttribute("lname", lname);
		Person p=new Person();
		p.setFirstName(fname);
		p.setLastName(lname);
		repository.save(p);
		model.addAttribute("person", p);
		return "greeting";
	}
	
	
	  @RequestMapping(value = "/prod")
	  @ResponseBody StringResponse getProduces(){
		  StringResponse s= new StringResponse();
		  s.setResponse("Attribute!");
		
	    return s;
	  }
	  


}
