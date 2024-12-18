package com.example.servingwebcontent;

import java.util.List;

import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;


public interface PersonRepository extends CrudRepository<Person, Long> {

  List<Person> findByFirstName(String firstName);
  List<Person> findByLastName(String lastName);

}
