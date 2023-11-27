package app.models.project;

public class ProjectAttribute {
    private long id;
    private String name;

    public ProjectAttribute() {

    }

    public ProjectAttribute(long id, String name) {
        this.id = id;
        this.name = name;
    }

    public long getId() {
        return id;
    }

    public String getName() {
        return name;
    }
}
