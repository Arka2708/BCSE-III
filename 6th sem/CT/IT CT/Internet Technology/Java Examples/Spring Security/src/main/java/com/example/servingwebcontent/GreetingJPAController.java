package com.example.servingwebcontent;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingJPAController {

	@Autowired
	PersonRepository repository1;
	
	
	@PostMapping("/greeting2")
	public List<Person> greeting2(@RequestParam(name="name",required=true) String fname) {
		List<Person> result= repository1.findByFirstName(fname);
		
		return result;
	}
}
