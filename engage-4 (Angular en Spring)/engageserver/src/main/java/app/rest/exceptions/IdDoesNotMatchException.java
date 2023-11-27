package app.rest.exceptions;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(HttpStatus.PRECONDITION_FAILED)
public class IdDoesNotMatchException extends RuntimeException{

    public IdDoesNotMatchException(String message) {
        super(message);
    }

}
