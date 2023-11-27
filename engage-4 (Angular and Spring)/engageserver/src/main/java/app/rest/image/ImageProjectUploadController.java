//package app.rest.image;
//
//import app.models.image.ImageProject;
//import app.models.project.Project;
//import app.repositories.Repository;
//import app.repositories.image.ImageProjectRepository;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.http.HttpStatus;
//import org.springframework.http.ResponseEntity;
//import org.springframework.web.bind.annotation.*;
//import org.springframework.web.multipart.MultipartFile;
//
//import org.springframework.web.bind.annotation.CrossOrigin;
//import org.springframework.web.bind.annotation.RequestMapping;
//import org.springframework.web.bind.annotation.RestController;
//
//import java.io.ByteArrayOutputStream;
//import java.io.IOException;
//import java.util.Optional;
//import java.util.zip.DataFormatException;
//import java.util.zip.Deflater;
//import java.util.zip.Inflater;
//
///**
// * @author Yazan
// * Date 13/05/2021 21:07
// */
//
//@RestController
//@CrossOrigin(origins = "http://localhost:4200")
//@RequestMapping(path = "projectImage")
//public class ImageProjectUploadController {
////    @Autowired
////    ImageProjectRepository imageRepository;
////    @Autowired
////    private Repository<Project> projectRepository;
////
////    @PostMapping("/upload/{projectId}")
////    public ResponseEntity.BodyBuilder uplaodImage(@PathVariable("projectId") int projectId, @RequestParam("imageFile") MultipartFile file) throws IOException {
////
//////        System.out.println("Original Image Byte Size - " + file.getBytes().length);
////        ImageProject img = new ImageProject(file.getOriginalFilename(), file.getContentType(),
////                compressBytes(file.getBytes()));
////
////        img.setProject(projectRepository.findById(projectId));
////
////
////        imageRepository.save(img);
////
////        return ResponseEntity.status(HttpStatus.OK);
////    }
////
//////    @GetMapping(path = { "/get/{imageName}" })
//////    public ImageModel getImage(@PathVariable("imageName") String imageName) throws IOException {
//////
//////        final Optional<ImageModel> retrievedImage = imageRepository.findByName(imageName);
//////        ImageModel img = new ImageModel(retrievedImage.get().getName(), retrievedImage.get().getType(),
//////                decompressBytes(retrievedImage.get().getPicByte()));
//////
//////        return img;
//////    }
////
////    @GetMapping(path = {"/get/{projectId}"})
////    public ImageProject getImageForUser(@PathVariable("projectId") long projectId) throws IOException {
////
////        final Optional<ImageProject> retrievedImage = imageRepository.findByProject_id(projectId);
////        ImageProject img = new ImageProject(retrievedImage.get().getName(), retrievedImage.get().getType(),
////                decompressBytes(retrievedImage.get().getPicByte()));
////
////        return img;
////    }
////
////    @GetMapping(path = {"/get/checkIfPhotoExist/{projectId}"})
////    public boolean checkIfPhotoExist(@PathVariable("projectId") long projectId) throws IOException {
////        return !imageRepository.findByProject_id(projectId).isEmpty();
////    }
////
////    // compress the image bytes before storing it in the database
////    public static byte[] compressBytes(byte[] data) {
////        Deflater deflater = new Deflater();
////        deflater.setInput(data);
////        deflater.finish();
////
////        ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);
////        byte[] buffer = new byte[1024];
////        while (!deflater.finished()) {
////            int count = deflater.deflate(buffer);
////            outputStream.write(buffer, 0, count);
////        }
////        try {
////            outputStream.close();
////        } catch (IOException e) {
////        }
////        // System.out.println("Compressed Image Byte Size - " + outputStream.toByteArray().length);
////
////        return outputStream.toByteArray();
////    }
////
////    // uncompress the image bytes before returning it to the angular application
////    public static byte[] decompressBytes(byte[] data) {
////        Inflater inflater = new Inflater();
////        inflater.setInput(data);
////        ByteArrayOutputStream outputStream = new ByteArrayOutputStream(data.length);
////        byte[] buffer = new byte[1024];
////        try {
////            while (!inflater.finished()) {
////                int count = inflater.inflate(buffer);
////                outputStream.write(buffer, 0, count);
////            }
////            outputStream.close();
////        } catch (IOException ioe) {
////        } catch (DataFormatException e) {
////        }
////        return outputStream.toByteArray();
////    }
//
//
//}
