import java.util.List;

class Artist {
    private String name;
    private List<Artist> members;
    private String origin;

    public Artist(String name, List<Artist> members, String origin) {
        this.name = name;
        this.members = members;
        this.origin = origin;
    }

    public String getName() {
        return name;
    }

    public List<Artist> getMembers() {
        return members;
    }

    public String getOrigin() {
        return origin;
    }
}
