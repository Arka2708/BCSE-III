import java.util.*;
import java.sql.*;

class CoffeeExpert {

    String getBrands(String color, String add_on, Connection con){
		String	result="";
	
	try{  
		
		Statement stmt=con.createStatement();  
		ResultSet rs=stmt.executeQuery(
			"select brand from CoffeeTypes where color = '" + color + "'");  
		while(rs.next())  
			result=result+rs.getString(1) ; 
		//con.close();  
		}catch(Exception e){ System.out.println(e);}  

	    return result;   
    }
 }
