package app.models;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

/**
 * @author Yazan
 * Date 11/05/2021 17:09
 */

@Entity
public
class Test {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;
    private String text;

    public Test() {
    }

    public Test(int id, String text) {
        this.id = id;
        this.text = text;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setText(String text) {
        this.text = text;
    }

    public int getId() {
        return id;
    }

    public String getText() {
        return text;
    }

    @Override
    public String toString() {
        return "test{" +
                "id=" + id +
                ", text='" + text + '\'' +
                '}';
    }
}


