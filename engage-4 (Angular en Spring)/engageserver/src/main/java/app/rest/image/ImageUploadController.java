package app.rest.image;

/**
 * @author Yazan
 * Date 12/05/2021 13:12
 */

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import java.util.Optional;
import java.util.zip.DataFormatException;
import java.util.zip.Deflater;
import java.util.zip.Inflater;

import app.models.image.ImageModel;
import app.models.image.ImageOrganisation;
import app.models.image.ImageProject;
import app.models.user.User;
import app.repositories.Repository;
import app.repositories.image.ImageRepository;
import app.repositories.image.OrganisationImageRepositroy;
import app.repositories.image.ProjectImageRepositroy;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.ResponseEntity.BodyBuilder;
import org.springframework.web.HttpMediaTypeNotAcceptableException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@CrossOrigin(origins = "http://localhost:4200")
@RequestMapping(path = "image")
public class ImageUploadController {

    //user image repo
    @Autowired
    ImageRepository imageRepository;

    //organisation image repo
    @Autowired
    OrganisationImageRepositroy organisationImageRepositroy;

    //project image repo
    @Autowired
    ProjectImageRepositroy projectImageRepositroy;

    @Autowired
    private Repository<User> usersRepository;

    //user upload and update method
    @PostMapping("/upload/{userId}")
    public BodyBuilder uplaodImage(@PathVariable("userId") int userId, @RequestParam("imageFile") MultipartFile file) throws IOException {

        ImageModel img = new ImageModel(file.getOriginalFilename(), file.getContentType(),
                compressBytes(file.getBytes()));
        img.setUser(usersRepository.findById(userId));
        try {
            ImageModel oldImage = imageRepository.findByUser_id(userId).get();
            oldImage.setPicByte(img.getPicByte());

            imageRepository.delete(oldImage);

        } catch (Exception e) {
            System.out.println(e.getCause());
        }


        imageRepository.save(img);

        return ResponseEntity.status(HttpStatus.OK);
    }

    @ResponseBody
    @ExceptionHandler(HttpMediaTypeNotAcceptableException.class)
    public String handleHttpMediaTypeNotAcceptableException() {
        return "";
    }

    //organisation photo upload and update method
    @PostMapping("/upload/organisation/{organisationId}")
    public BodyBuilder uplaodImageOrganisatopn(@PathVariable("organisationId") long organisationId, @RequestParam("imageFile") MultipartFile file) throws IOException {

        ImageOrganisation img = new ImageOrganisation(file.getOriginalFilename(), file.getContentType(),
                compressBytes(file.getBytes()));

        img.setOrganisationId(organisationId);
        try {
            ImageOrganisation oldImage = organisationImageRepositroy.findByOrganisationId(organisationId).get();
            oldImage.setPicByte(img.getPicByte());

            organisationImageRepositroy.delete(oldImage);

        } catch (Exception e) {
            System.out.println(e.getCause());
        }


        organisationImageRepositroy.save(img);

        return ResponseEntity.status(HttpStatus.OK);
    }

    //project photo upload and update method
    @PostMapping("/upload/project/{projectId}")
    public BodyBuilder uplaodImageProject(@PathVariable("projectId") long projectId, @RequestParam("imageFile") MultipartFile file) throws IOException {

        ImageProject img = new ImageProject(file.getOriginalFilename(), file.getContentType(),
                compressBytes(file.getBytes()));

        img.setProjectId(projectId);
        try {
            ImageProject oldImage = projectImageRepositroy.findByProjectId(projectId).get();
            oldImage.setPicByte(img.getPicByte());

            projectImageRepositroy.delete(oldImage);

        } catch (Exception e) {
            System.out.println(e.getCause());
        }


        projectImageRepositroy.save(img);

        return ResponseEntity.status(HttpStatus.OK);
    }

    //getting photo for user
    @GetMapping(path = {"/get/{userId}"})
    public ImageModel getImageForUser(@PathVariable("userId") long userId) throws IOException {

        final Optional<ImageModel> retrievedImage = imageRepository.findByUser_id(userId);
        ImageModel img = new ImageModel(retrievedImage.get().getName(), retrievedImage.get().getType(),
                decompressBytes(retrievedImage.get().getPicByte()));

        return img;
    }

    //getting photo for organisatoin
    @GetMapping(path = "/get/organisationImage/{organisatoinId}")
    public ImageOrganisation getImageForOrganistion(@PathVariable("organisatoinId") long organisatoinId) throws IOException {
        System.out.println("getting image for organisation");

        final Optional<ImageOrganisation> retrievedImage = organisationImageRepositroy.findByOrganisationId(organisatoinId);
        ImageOrganisation img = new ImageOrganisation(retrievedImage.get().getName(), retrievedImage.get().getType(),
                decompressBytes(retrievedImage.get().getPicByte()));

        return img;
    }

    //getting photo for project
    @GetMapping(path = "/get/projectImage/{projectId}")
    public ImageProject getImageForProject(@PathVariable("projectId") long projectId) throws IOException {

        final Optional<ImageProject> retrievedImage = projectImageRepositroy.findByProjectId(projectId);
        ImageProject img = new ImageProject(retrievedImage.get().getName(), retrievedImage.get().getType(),
                decompressBytes(retrievedImage.get().getPicByte()));

        return img;
    }

    //checking if photo exist for user
    @GetMapping(path = {"/get/checkIfPhotoExist/{userId}"})
    public boolean checkIfPhotoExist(@PathVariable("userId") long userId) throws IOException {
        return !imageRepository.findByUser_id(userId).isEmpty();
    }
    //checking if photo exist for organisation

    @GetMapping(path = "/get/checkIfOrgansationPhotoExist/{organisationId}")
    public boolean checkIfPhotoExistForOrganisation(@PathVariable("organisationId") long organisationId) throws IOException {
        return organisationImageRepositroy.findByOrganisationId(organisationId).isPresent();
    }

    //checking if photo exist for project
    @GetMapping(path = "/get/checkIfProjectPhotoExist/{projectId}")
    public boolean checkIfPhotoExistForProject(@PathVariable("projectId") long projectId) throws IOException {
        return projectImageRepositroy.findByProjectId(projectId).isPresent();
    }

    @DeleteMapping("userImage/{id}")
    public ResponseEntity<Boolean> deleteUserImage(@PathVariable long id) {

        if (imageRepository.findByUser_id(id).isPresent()){
            ImageModel oldImage = imageRepository.findByUser_id(id).get();
            imageRepository.delete(oldImage);
            return ResponseEntity.ok(true);

        }else {
            return ResponseEntity.ok(false);
        }




    }
    @DeleteMapping("organisationImage/{id}")
    public ResponseEntity<Boolean> deleteOrganisationImage(@PathVariable long id) {

        if (organisationImageRepositroy.findByOrganisationId(id).isPresent()){
            ImageOrganisation oldImage = organisationImageRepositroy.findByOrganisationId(id).get();
            organisationImageRepositroy.delete(oldImage);
            return ResponseEntity.ok(true);
        }else {
            return ResponseEntity.ok(false);
        }


    }
    @DeleteMapping("projectImage/{id}")
    public ResponseEntity<Boolean> deleteProjectImage(@PathVariable long id) {
        
        if (projectImageRepositroy.findByProjectId(id).isPresent()){
            ImageProject oldImage = projectImageRepositroy.findByProjectId(id).get();
            projectImageRepositroy.delete(oldImage);
            return ResponseEntity.ok(true);
        }else {
            return ResponseEntity.ok(false);
        }

    }

    // compress the image bytes before storing it in the database
    public static byte[] compressBytes(byte[] data) {
        Deflater deflater = new Deflater();
        deflater.setInput(data);
        deflater.finish();

        ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);
        byte[] buffer = new byte[1024];
        while (!deflater.finished()) {
            int count = deflater.deflate(buffer);
            outputStream.write(buffer, 0, count);
        }
        try {
            outputStream.close();
        } catch (IOException e) {
        }
        // System.out.println("Compressed Image Byte Size - " + outputStream.toByteArray().length);

        return outputStream.toByteArray();
    }

    // uncompress the image bytes before returning it to the angular application
    public static byte[] decompressBytes(byte[] data) {
        Inflater inflater = new Inflater();
        inflater.setInput(data);
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);
        byte[] buffer = new byte[1024];
        try {
            while (!inflater.finished()) {
                int count = inflater.inflate(buffer);
                outputStream.write(buffer, 0, count);
            }
            outputStream.close();
        } catch (IOException ioe) {
        } catch (DataFormatException e) {
        }
        return outputStream.toByteArray();
    }
}