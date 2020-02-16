package MyMapReduce;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Reader {

    private final Path rootPath;

    public Reader(Path rootPath) {
        this.rootPath = rootPath;
    }

    public Stream<Pair<String, List<String>>> read() throws IOException {
        List<Path> paths = Files.walk(rootPath).collect(Collectors.toList());
        return paths.stream()
                .filter(Files::isRegularFile)
                .filter(path -> path.getFileName().toString().endsWith(".txt"))
                .map(path -> new Pair<String, List<String>>(path.getFileName().toString(),
                        myReadAllLines(path)));
    }

    private List<String> myReadAllLines(Path path) {
        try {
            return Files.readAllLines(path, StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
