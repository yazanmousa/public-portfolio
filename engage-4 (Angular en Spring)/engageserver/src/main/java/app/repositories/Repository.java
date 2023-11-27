package app.repositories;

import app.models.user.User;

import java.util.List;

public interface Repository<T> {

    List<T> findAll();
    T findById(long id);
    T save(T object);
    boolean deleteById(long id);

}
