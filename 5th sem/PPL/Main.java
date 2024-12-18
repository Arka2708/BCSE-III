import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        // Creating a list of artists
        List<Artist> artists = new ArrayList<>();

        // Example 1: Solo artist
        Artist soloArtist = new Artist("John Doe", new ArrayList<>(), "New York");
        artists.add(soloArtist);

        // Example 2: Band from Kolkata
        Artist kolkataBand = new Artist("Kolkata Band", List.of(
                new Artist("Member1", new ArrayList<>(), "Kolkata"),
                new Artist("Member2", new ArrayList<>(), "Kolkata"),
                new Artist("Member3", new ArrayList<>(), "Kolkata")
        ), "Kolkata");
        artists.add(kolkataBand);

        // Example 3: Band from London
        Artist londonBand = new Artist("London Band", List.of(
                new Artist("MemberA", new ArrayList<>(), "London"),
                new Artist("MemberB", new ArrayList<>(), "London")
        ), "London");
        artists.add(londonBand);

        // (a) Internal iteration to find the total count of members from Kolkata
        long total = artists.stream()
                .filter(artist -> "kolkata".equalsIgnoreCase(artist.getOrigin()))
                .flatMap(artist -> artist.getMembers().stream())
                .count();

        System.out.println("Total members from Kolkata: " + total);

        // (b) Find the bands with the most members
        artists.stream()
                .max((a1, a2) -> Integer.compare(a1.getMembers().size(), a2.getMembers().size()))
                .ifPresent(artist -> System.out.println("Band with most members: " + artist.getName()));
    }
}