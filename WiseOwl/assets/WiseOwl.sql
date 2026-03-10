-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 10, 2026 at 04:12 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pycharm`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminacc_code`
--

CREATE TABLE `adminacc_code` (
  `id` int(11) NOT NULL,
  `access_code` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adminacc_code`
--

INSERT INTO `adminacc_code` (`id`, `access_code`) VALUES
(2, 'Admin45'),
(1, 'ADmin5'),
(3, 'LibAD34');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `author` varchar(100) NOT NULL,
  `genre` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `total_copies` int(11) DEFAULT 1,
  `available_copies` int(11) DEFAULT 1,
  `location` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `author`, `genre`, `description`, `total_copies`, `available_copies`, `location`) VALUES
(1, 'Noli Me Tangere', 'Dr. Jose Rizal', 'Fiction', 'A novel about Philippine society during Spanish colonization', 5, 2, 'Filipiniana Section A1'),
(2, 'El Filibusterismo', 'Dr. Jose Rizal', 'Fiction', 'Sequel to Noli Me Tangere', 5, 4, 'Filipiniana Section A1'),
(3, 'Florante at Laura', 'Francisco Balagtas', 'Poetry', 'A classic Philippine literary masterpiece', 3, 3, 'Filipiniana Section A2'),
(4, 'Ibong Adarna', 'Anonymous', 'Folklore', 'A famous epic about a magical bird', 4, 2, 'Filipiniana Section A2'),
(5, 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 'Epic high fantasy novel', 3, 0, 'Fiction Section B1'),
(6, 'Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 'Fantasy', 'First book in the Harry Potter series', 4, 4, 'Fiction Section B1'),
(7, 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 'Fantasy', 'Second book in the Harry Potter series', 4, 4, 'Fiction Section B1'),
(8, 'Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 'Fantasy', 'Third book in the Harry Potter series', 4, 4, 'Fiction Section B1'),
(9, 'Harry Potter and the Goblet of Fire', 'J.K. Rowling', 'Fantasy', 'Fourth book in the Harry Potter series', 4, 4, 'Fiction Section B2'),
(10, 'Harry Potter and the Order of the Phoenix', 'J.K. Rowling', 'Fantasy', 'Fifth book in the Harry Potter series', 4, 4, 'Fiction Section B2'),
(11, 'Harry Potter and the Half-Blood Prince', 'J.K. Rowling', 'Fantasy', 'Sixth book in the Harry Potter series', 4, 3, 'Fiction Section B2'),
(12, 'Harry Potter and the Deathly Hallows', 'J.K. Rowling', 'Fantasy', 'Seventh book in the Harry Potter series', 4, 4, 'Fiction Section B2'),
(13, 'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'Adventure story about Bilbo Baggins', 3, 1, 'Fiction Section B3'),
(14, 'The Two Towers', 'J.R.R. Tolkien', 'Fantasy', 'Second volume of The Lord of the Rings', 3, 2, 'Fiction Section B3'),
(15, 'The Return of the King', 'J.R.R. Tolkien', 'Fantasy', 'Third volume of The Lord of the Rings', 3, 1, 'Fiction Section B3'),
(16, '1984', 'George Orwell', 'Dystopian', 'A novel about totalitarianism and surveillance', 3, 1, 'Fiction Section C1'),
(17, 'Animal Farm', 'George Orwell', 'Satire', 'An allegorical novella about Soviet communism', 3, 3, 'Fiction Section C1'),
(18, 'To Kill a Mockingbird', 'Harper Lee', 'Classic', 'A story about racial injustice in the American South', 4, 4, 'Classics Section D1'),
(19, 'Pride and Prejudice', 'Jane Austen', 'Romance', 'A classic romantic novel', 3, 3, 'Classics Section D1'),
(20, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'A story about the Jazz Age', 4, 4, 'Classics Section D1'),
(21, 'Moby Dick', 'Herman Melville', 'Adventure', 'A whaling captain\'s obsession with a white whale', 2, 1, 'Classics Section D2'),
(22, 'War and Peace', 'Leo Tolstoy', 'Historical Fiction', 'Epic novel about Russian society', 2, 1, 'Classics Section D2'),
(23, 'Crime and Punishment', 'Fyodor Dostoevsky', 'Psychological Fiction', 'A story about guilt and redemption', 3, 2, 'Classics Section D2'),
(24, 'The Adventures of Huckleberry Finn', 'Mark Twain', 'Adventure', 'A boy\'s journey along the Mississippi River', 3, 2, 'Classics Section D3'),
(25, 'The Catcher in the Rye', 'J.D. Salinger', 'Coming-of-age', 'A story about teenage alienation', 3, 2, 'Classics Section D3'),
(26, 'The Da Vinci Code', 'Dan Brown', 'Mystery', 'A mystery thriller about religious conspiracies', 5, 3, 'Mystery Section E1'),
(27, 'Angels & Demons', 'Dan Brown', 'Mystery', 'A thriller involving the Illuminati', 4, 3, 'Mystery Section E1'),
(28, 'The Lost Symbol', 'Dan Brown', 'Mystery', 'A mystery set in Washington D.C.', 4, 4, 'Mystery Section E1'),
(29, 'Inferno', 'Dan Brown', 'Mystery', 'A thriller based on Dante\'s Inferno', 4, 4, 'Mystery Section E1'),
(30, 'The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Mystery', 'A mystery novel about a missing person', 3, 3, 'Mystery Section E2'),
(31, 'Gone Girl', 'Gillian Flynn', 'Thriller', 'A psychological thriller about a missing wife', 4, 4, 'Thriller Section F1'),
(32, 'The Silent Patient', 'Alex Michaelides', 'Thriller', 'A psychological thriller about a silent patient', 5, 5, 'Thriller Section F1'),
(33, 'The Woman in the Window', 'A.J. Finn', 'Thriller', 'A thriller about an agoraphobic woman', 4, 4, 'Thriller Section F1'),
(34, 'The Girl on the Train', 'Paula Hawkins', 'Thriller', 'A psychological thriller set on a train', 4, 4, 'Thriller Section F2'),
(35, 'The Shining', 'Stephen King', 'Horror', 'A horror novel about a haunted hotel', 3, 0, 'Horror Section G1'),
(36, 'It', 'Stephen King', 'Horror', 'A horror novel about a shape-shifting entity', 3, 2, 'Horror Section G1'),
(37, 'Pet Sematary', 'Stephen King', 'Horror', 'A horror novel about a pet cemetery', 3, 3, 'Horror Section G1'),
(38, 'The Stand', 'Stephen King', 'Horror', 'A post-apocalyptic horror novel', 2, 2, 'Horror Section G2'),
(39, 'Dracula', 'Bram Stoker', 'Horror', 'Classic Gothic horror novel', 3, 3, 'Horror Section G2'),
(40, 'Frankenstein', 'Mary Shelley', 'Horror', 'A story about a scientist creating a monster', 3, 3, 'Horror Section G2'),
(41, 'The Exorcist', 'William Peter Blatty', 'Horror', 'A horror novel about demonic possession', 2, 2, 'Horror Section G3'),
(42, 'Dune', 'Frank Herbert', 'Science Fiction', 'Epic science fiction novel set on a desert planet', 3, 3, 'Sci-Fi Section H1'),
(43, 'Foundation', 'Isaac Asimov', 'Science Fiction', 'A science fiction novel about a galactic empire', 3, 3, 'Sci-Fi Section H1'),
(44, 'I, Robot', 'Isaac Asimov', 'Science Fiction', 'A collection of robot stories', 3, 3, 'Sci-Fi Section H1'),
(45, 'Neuromancer', 'William Gibson', 'Cyberpunk', 'A pioneering cyberpunk novel', 2, 2, 'Sci-Fi Section H2'),
(46, 'Ender\'s Game', 'Orson Scott Card', 'Science Fiction', 'A story about a child trained for war', 4, 4, 'Sci-Fi Section H2'),
(47, 'The Martian', 'Andy Weir', 'Science Fiction', 'An astronaut stranded on Mars', 5, 5, 'Sci-Fi Section H2'),
(48, 'Brave New World', 'Aldous Huxley', 'Dystopian', 'A dystopian novel about a futuristic society', 3, 3, 'Sci-Fi Section H3'),
(49, 'Fahrenheit 451', 'Ray Bradbury', 'Dystopian', 'A novel about book burning', 3, 3, 'Sci-Fi Section H3'),
(50, 'The Hunger Games', 'Suzanne Collins', 'Dystopian', 'A dystopian novel about a televised death match', 5, 5, 'Young Adult Section I1'),
(51, 'Catching Fire', 'Suzanne Collins', 'Dystopian', 'Second book in The Hunger Games trilogy', 5, 5, 'Young Adult Section I1'),
(52, 'Mockingjay', 'Suzanne Collins', 'Dystopian', 'Third book in The Hunger Games trilogy', 5, 5, 'Young Adult Section I1'),
(53, 'Twilight', 'Stephenie Meyer', 'Romance', 'A vampire romance novel', 4, 4, 'Young Adult Section I2'),
(54, 'New Moon', 'Stephenie Meyer', 'Romance', 'Second book in the Twilight series', 4, 4, 'Young Adult Section I2'),
(55, 'Eclipse', 'Stephenie Meyer', 'Romance', 'Third book in the Twilight series', 4, 3, 'Young Adult Section I2'),
(56, 'Breaking Dawn', 'Stephenie Meyer', 'Romance', 'Fourth book in the Twilight series', 4, 4, 'Young Adult Section I2'),
(57, 'The Fault in Our Stars', 'John Green', 'Young Adult', 'A story about teenage cancer patients', 5, 5, 'Young Adult Section I3'),
(58, 'Looking for Alaska', 'John Green', 'Young Adult', 'A coming-of-age novel', 4, 4, 'Young Adult Section I3'),
(59, 'Paper Towns', 'John Green', 'Young Adult', 'A mystery about a missing girl', 4, 3, 'Young Adult Section I3'),
(60, 'The Maze Runner', 'James Dashner', 'Young Adult', 'Teens trapped in a maze', 4, 4, 'Young Adult Section I4'),
(61, 'The Scorch Trials', 'James Dashner', 'Young Adult', 'Second book in The Maze Runner series', 4, 4, 'Young Adult Section I4'),
(62, 'The Death Cure', 'James Dashner', 'Young Adult', 'Third book in The Maze Runner series', 4, 4, 'Young Adult Section I4'),
(63, 'Divergent', 'Veronica Roth', 'Young Adult', 'A dystopian novel about factions', 5, 5, 'Young Adult Section I5'),
(64, 'Insurgent', 'Veronica Roth', 'Young Adult', 'Second book in the Divergent series', 6, 5, 'Young Adult Section I5'),
(65, 'Allegiant', 'Veronica Roth', 'Young Adult', 'Third book in the Divergent series', 5, 5, 'Young Adult Section I5'),
(66, 'The Alchemist', 'Paulo Coelho', 'Philosophical Fiction', 'A story about following your dreams', 5, 5, 'General Section J1'),
(67, 'The Little Prince', 'Antoine de Saint-Exupéry', 'Philosophical Fiction', 'A poetic tale about friendship', 4, 1, 'General Section J1'),
(68, 'The Old Man and the Sea', 'Ernest Hemingway', 'Literary Fiction', 'A story about an aging fisherman', 3, 3, 'General Section J1'),
(69, 'For Whom the Bell Tolls', 'Ernest Hemingway', 'Literary Fiction', 'A novel about the Spanish Civil War', 2, 2, 'General Section J2'),
(70, 'The Sun Also Rises', 'Ernest Hemingway', 'Literary Fiction', 'A novel about the Lost Generation', 2, 2, 'General Section J2'),
(71, 'A Farewell to Arms', 'Ernest Hemingway', 'Literary Fiction', 'A love story during World War I', 2, 2, 'General Section J2'),
(72, 'One Hundred Years of Solitude', 'Gabriel García Márquez', 'Magical Realism', 'A multi-generational story', 2, 2, 'General Section J3'),
(73, 'Love in the Time of Cholera', 'Gabriel García Márquez', 'Magical Realism', 'A love story spanning decades', 2, 2, 'General Section J3'),
(74, 'The House of the Spirits', 'Isabel Allende', 'Magical Realism', 'A family saga with magical elements', 2, 2, 'General Section J3'),
(75, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Non-Fiction', 'A history of the human species', 4, 4, 'Non-Fiction Section K1'),
(76, 'Homo Deus: A Brief History of Tomorrow', 'Yuval Noah Harari', 'Non-Fiction', 'A vision of the future', 3, 3, 'Non-Fiction Section K1'),
(77, '21 Lessons for the 21st Century', 'Yuval Noah Harari', 'Non-Fiction', 'Essays on contemporary issues', 3, 2, 'Non-Fiction Section K1'),
(79, 'The Selfish Gene', 'Richard Dawkins', 'Science', 'A book about evolutionary biology', 2, 2, 'Science Section L1'),
(80, 'The Origin of Species', 'Charles Darwin', 'Science', 'Foundation of evolutionary biology', 1, 1, 'Science Section L1'),
(81, 'Cosmos', 'Carl Sagan', 'Science', 'A book about the universe', 2, 2, 'Science Section L2'),
(82, 'The Elegant Universe', 'Brian Greene', 'Science', 'A book about string theory', 1, 1, 'Science Section L2'),
(83, 'The Power of Habit', 'Charles Duhigg', 'Self-Help', 'Why we do what we do', 4, 4, 'Self-Help Section M1'),
(84, 'Atomic Habits', 'James Clear', 'Self-Help', 'Tiny changes, remarkable results', 5, 5, 'Self-Help Section M1'),
(85, 'The 7 Habits of Highly Effective People', 'Stephen Covey', 'Self-Help', 'Personal development classic', 3, 3, 'Self-Help Section M1'),
(86, 'How to Win Friends and Influence People', 'Dale Carnegie', 'Self-Help', 'Interpersonal skills guide', 4, 3, 'Self-Help Section M2'),
(87, 'Think and Grow Rich', 'Napoleon Hill', 'Self-Help', 'Personal success philosophy', 3, 3, 'Self-Help Section M2'),
(88, 'The Subtle Art of Not Giving a F*ck', 'Mark Manson', 'Self-Help', 'A counterintuitive approach to living', 5, 5, 'Self-Help Section M2'),
(89, 'Becoming', 'Michelle Obama', 'Biography', 'Memoir of the former First Lady', 4, 4, 'Biography Section N1'),
(90, 'Steve Jobs', 'Walter Isaacson', 'Biography', 'Biography of Apple co-founder', 3, 3, 'Biography Section N1'),
(91, 'Einstein: His Life and Universe', 'Walter Isaacson', 'Biography', 'Biography of Albert Einstein', 2, 2, 'Biography Section N1'),
(92, 'Leonardo da Vinci', 'Walter Isaacson', 'Biography', 'Biography of the Renaissance master', 2, 2, 'Biography Section N2'),
(93, 'The Diary of a Young Girl', 'Anne Frank', 'Biography', 'Diary of a Jewish girl during WWII', 4, 4, 'Biography Section N2'),
(94, 'Long Walk to Freedom', 'Nelson Mandela', 'Biography', 'Autobiography of Nelson Mandela', 2, 2, 'Biography Section N2'),
(95, 'The Art of War', 'Sun Tzu', 'Philosophy', 'Ancient Chinese military treatise', 3, 2, 'Philosophy Section O1'),
(96, 'Meditations', 'Marcus Aurelius', 'Philosophy', 'Stoic philosophy writings', 2, 0, 'Philosophy Section O1'),
(97, 'Thus Spoke Zarathustra', 'Friedrich Nietzsche', 'Philosophy', 'Philosophical novel', 1, 1, 'Philosophy Section O1'),
(98, 'The Republic', 'Plato', 'Philosophy', 'Socratic dialogue about justice', 2, 2, 'Philosophy Section O2'),
(99, 'Beyond Good and Evil', 'Friedrich Nietzsche', 'Philosophy', 'Critique of traditional morality', 1, 1, 'Philosophy Section O2'),
(100, 'The Communist Manifesto', 'Karl Marx', 'Political Science', 'Political pamphlet', 2, 2, 'Political Science Section P1'),
(101, 'The Prince', 'Niccolò Machiavelli', 'Political Science', 'Political treatise on power', 2, 2, 'Political Science Section P1'),
(102, 'The Social Contract', 'Jean-Jacques Rousseau', 'Political Science', 'Work on political philosophy', 1, 1, 'Political Science Section P1');

-- --------------------------------------------------------

--
-- Table structure for table `borrow_records`
--

CREATE TABLE `borrow_records` (
  `id` int(11) NOT NULL,
  `member_id` varchar(50) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `book_title` varchar(200) DEFAULT NULL,
  `borrow_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `condition_on_return` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Borrowed',
  `processed_by` varchar(50) DEFAULT NULL,
  `processed_by_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `borrow_records`
--

INSERT INTO `borrow_records` (`id`, `member_id`, `book_id`, `book_title`, `borrow_date`, `due_date`, `return_date`, `condition_on_return`, `status`, `processed_by`, `processed_by_name`) VALUES
(1, '202503', 13, 'The Hobbit', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(2, '202523', 15, 'The Return of the King', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(3, '202502', 5, 'The Lord of the Rings', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(4, '200601', 5, 'The Lord of the Rings', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(5, '200601', 16, '1984', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(6, '202510', 16, '1984', '2026-02-27', '2026-03-13', '2026-03-03', 'Good', 'Returned', NULL, NULL),
(7, '202506', 55, 'Eclipse', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(8, '202503', 59, 'Paper Towns', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(9, '202505', 95, 'The Art of War', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(10, '202507', 67, 'The Little Prince', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(11, '202503', 67, 'The Little Prince', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(12, '202501', 26, 'The Da Vinci Code', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(13, '202511', 23, 'Crime and Punishment', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(14, '202512', 15, 'The Return of the King', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(15, '202514', 35, 'The Shining', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(16, '202522', 36, 'It', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(17, '202521', 86, 'How to Win Friends and Influence People', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(18, '202520', 27, 'Angels & Demons', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(19, '202562', 24, 'The Adventures of Huckleberry Finn', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(20, '202575', 24, 'The Adventures of Huckleberry Finn', '2026-02-27', '2026-03-13', '2026-03-04', 'Fair', 'Returned', NULL, NULL),
(21, '202560', 32, 'The Silent Patient', '2026-02-27', '2026-03-13', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(22, '202503', 26, 'The Da Vinci Code', '2026-02-27', '2026-03-13', '2026-03-03', 'Poor', 'Returned', NULL, NULL),
(23, '202503', 26, 'The Da Vinci Code', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(24, '202503', 1, 'Noli Me Tangere', '2026-02-27', '2026-03-13', '2026-03-03', 'Good', 'Returned', NULL, NULL),
(25, '202503', 1, 'Noli Me Tangere', '2026-02-27', '2026-03-13', '2026-03-03', 'Poor', 'Returned', NULL, NULL),
(26, '202503', 1, 'Noli Me Tangere', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(27, '202503', 1, 'Noli Me Tangere', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(28, '202503', 1, 'Noli Me Tangere', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(29, '202507', 11, 'Harry Potter and the Half-Blood Prince', '2026-02-27', '2026-03-13', '2026-03-10', 'Good', 'Returned', '200605', 'Wenafe Magayawa'),
(30, '202507', 11, 'Harry Potter and the Half-Blood Prince', '2026-02-27', '2026-03-13', NULL, NULL, 'Borrowed', NULL, NULL),
(31, '200601', 53, 'Twilight', '2026-03-01', '2026-03-04', '2026-03-09', 'Good', 'Returned', NULL, NULL),
(32, '200601', 84, 'Atomic Habits', '2026-03-01', '2026-03-03', '2026-03-09', 'Good', 'Returned', NULL, NULL),
(33, '202503', 95, 'The Art of War', '2026-03-01', '2026-03-02', '2026-03-09', 'Good', 'Returned', NULL, NULL),
(34, '200601', 96, 'Meditations', '2026-03-01', '2026-03-15', NULL, NULL, 'Borrowed', NULL, NULL),
(35, '202506', 32, 'The Silent Patient', '2026-03-01', '2026-03-02', '2026-03-09', 'Good', 'Returned', NULL, NULL),
(36, '202507', 36, 'It', '2026-03-01', '2026-03-02', '2026-03-03', 'Good', 'Returned', NULL, NULL),
(37, '202507', 23, 'Crime and Punishment', '2026-03-01', '2026-03-02', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(38, '202503', 89, 'Becoming', '2026-03-03', '2026-03-04', '2026-03-09', 'Good', 'Returned', NULL, NULL),
(39, '202598', 35, 'The Shining', '2026-03-03', '2026-03-04', '2026-03-09', 'Good', 'Returned', NULL, NULL),
(40, '202509', 96, 'Meditations', '2026-03-03', '2026-03-17', NULL, NULL, 'Borrowed', NULL, NULL),
(41, '200601', 16, '1984', '2026-03-03', '2026-03-17', NULL, NULL, 'Borrowed', NULL, NULL),
(42, '200601', 71, 'A Farewell to Arms', '2026-03-03', '2026-03-17', '2026-03-03', 'Good', 'Returned', NULL, NULL),
(43, '200601', 16, '1984', '2026-03-03', '2026-03-17', NULL, NULL, 'Borrowed', NULL, NULL),
(44, '200601', 16, '1984', '2026-03-03', '2026-03-17', NULL, NULL, 'Borrowed', NULL, NULL),
(45, '202596', 71, 'A Farewell to Arms', '2026-03-04', '2026-03-18', '2026-03-06', 'Good', 'Returned', NULL, NULL),
(47, '202587', 67, 'The Little Prince', '2026-03-04', '2026-03-18', NULL, NULL, 'Borrowed', NULL, NULL),
(48, '202596', 35, 'The Shining', '2026-03-04', '2026-03-18', NULL, NULL, 'Borrowed', NULL, NULL),
(49, '202546', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(50, '202564', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(51, '202547', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(52, '202536', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(53, '202594', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(54, '202594', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(55, '202595', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(56, '202595', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(57, '202595', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(58, '202594', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(59, '202594', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-09', 'Good', 'Returned', '200605', 'Wenafe Magayawa'),
(60, '202548', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(61, '202563', 4, 'Ibong Adarna', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(62, '202537', 16, '1984', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(63, '202537', 15, 'The Return of the King', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(64, '202507', 16, '1984', '2026-03-04', '2026-03-18', '2026-03-04', 'Good', 'Returned', NULL, NULL),
(65, '202534', 16, '1984', '2026-03-06', '2026-03-20', '2026-03-09', 'Good', 'Returned', '200605', 'Wenafe Magayawa'),
(66, '202564', 4, 'Ibong Adarna', '2026-03-09', '2026-03-23', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(67, '202503', 4, 'Ibong Adarna', '2026-03-09', '2026-03-10', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(68, '202507', 2, 'El Filibusterismo', '2026-03-09', '2026-03-10', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(69, '202511', 5, 'The Lord of the Rings', '2026-03-09', '2026-03-10', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(70, '202517', 13, 'The Hobbit', '2026-03-09', '2026-03-10', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(71, '202514', 14, 'The Two Towers', '2026-03-09', '2026-03-10', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(72, '202504', 21, 'Moby Dick', '2026-03-09', '2026-03-10', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(73, '202504', 22, 'War and Peace', '2026-03-09', '2026-03-10', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(74, '202505', 77, '21 Lessons for the 21st Century', '2026-03-09', '2026-03-12', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(75, '202505', 25, 'The Catcher in the Rye', '2026-03-09', '2026-03-12', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa'),
(76, '202503', 35, 'The Shining', '2026-03-10', '2026-03-13', NULL, NULL, 'Borrowed', '200605', 'Wenafe Magayawa');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(2, 'Library Admin'),
(1, 'Library User');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `member_id` varchar(50) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `join_date` date DEFAULT curdate(),
  `borrowed_count` int(11) DEFAULT 0,
  `overdue_count` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `user_name`, `member_id`, `category_id`, `email`, `phone`, `join_date`, `borrowed_count`, `overdue_count`) VALUES
(1, 'Wenafe Magayawa', '200605', 2, 'wenafe@email.com', '', '2026-02-18', 0, 0),
(2, 'Wena Magayawa', '200601', 1, 'wena@email.com', '', '2026-02-18', 9, 0),
(3, 'Angela Lacman', '202501', 1, 'angela@email.com', '', '2026-02-18', 1, 0),
(4, 'Ryan Mahinay', '202502', 2, 'ryan@email.com', '', '2026-02-18', 1, 0),
(5, 'Blyte Hinay', '202503', 1, 'blyte@email.com', '', '2026-02-18', 14, 0),
(6, 'Carl Jhon Paul Masayon', '202504', 1, 'carl@email.com', '', '2026-02-18', 2, 0),
(7, 'Carl David Campos', '202505', 1, 'david@email.com', '', '2026-02-18', 3, 0),
(8, 'Jules Henri Reyes', '202506', 1, 'jules@email.com', '', '2026-02-18', 2, 0),
(9, 'Wince Samillano', '202507', 1, 'wince@email.com', '', '2026-02-18', 7, 0),
(10, 'Hannah Leah Fabracuer', '202508', 2, 'hannah@email.com', '', '2026-02-18', 0, 0),
(11, 'Maria Santos', '202509', 1, 'maria.santos@email.com', '', '2026-02-18', 1, 0),
(12, 'Jose Reyes', '202510', 2, 'jose.reyes@email.com', '', '2026-02-18', 1, 0),
(13, 'Ana Gonzales', '202511', 1, 'ana.gonzales@email.com', '', '2026-02-18', 2, 0),
(14, 'Pedro Cruz', '202512', 1, 'pedro.cruz@email.com', '', '2026-02-18', 1, 0),
(15, 'Luisa Fernandez', '202513', 2, 'luisa.fernandez@email.com', '', '2026-02-18', 0, 0),
(16, 'Miguel Lopez', '202514', 1, 'miguel.lopez@email.com', '', '2026-02-18', 2, 0),
(17, 'Isabella Garcia', '202515', 1, 'isabella.garcia@email.com', '', '2026-02-18', 0, 0),
(18, 'Ramon Torres', '202516', 2, 'ramon.torres@email.com', '', '2026-02-18', 0, 0),
(19, 'Sofia Villanueva', '202517', 1, 'sofia.villanueva@email.com', '', '2026-02-18', 1, 0),
(20, 'Diego Ramos', '202518', 1, 'diego.ramos@email.com', '', '2026-02-18', 0, 0),
(21, 'Carmen Flores', '202519', 2, 'carmen.flores@email.com', '', '2026-02-18', 0, 0),
(22, 'Antonio Rivera', '202520', 1, 'antonio.rivera@email.com', '', '2026-02-18', 1, 0),
(23, 'Patricia Mendoza', '202521', 1, 'patricia.mendoza@email.com', '', '2026-02-18', 1, 0),
(24, 'Fernando Castro', '202522', 1, 'fernando.castro@email.com', '', '2026-02-18', 1, 0),
(25, 'Gloria Dela Cruz', '202523', 2, 'gloria.delacruz@email.com', '', '2026-02-18', 1, 0),
(26, 'Ricardo Navarro', '202524', 1, 'ricardo.navarro@email.com', '', '2026-02-18', 0, 0),
(27, 'Luzviminda Aquino', '202525', 2, 'luzviminda.aquino@email.com', '', '2026-02-18', 0, 0),
(28, 'Emmanuel Guzman', '202526', 1, 'emmanuel.guzman@email.com', '', '2026-02-18', 0, 0),
(29, 'Teresa Morales', '202527', 1, 'teresa.morales@email.com', '', '2026-02-18', 0, 0),
(30, 'Rafael Santiago', '202528', 1, 'rafael.santiago@email.com', '', '2026-02-18', 0, 0),
(31, 'Cristina Alvarez', '202529', 2, 'cristina.alvarez@email.com', '', '2026-02-18', 0, 0),
(32, 'Jorge Romero', '202530', 1, 'jorge.romero@email.com', '', '2026-02-18', 0, 0),
(33, 'Mercedes Castillo', '202531', 1, 'mercedes.castillo@email.com', '', '2026-02-18', 0, 0),
(34, 'Francisco Ortega', '202532', 1, 'francisco.ortega@email.com', '', '2026-02-18', 0, 0),
(35, 'Adelaida Marcelo', '202533', 2, 'adelaida.marcelo@email.com', '', '2026-02-18', 0, 0),
(36, 'Rodrigo Benitez', '202534', 1, 'rodrigo.benitez@email.com', '', '2026-02-18', 1, 0),
(37, 'Esperanza Dimagiba', '202535', 2, 'esperanza.dimagiba@email.com', '', '2026-02-18', 0, 0),
(38, 'Armando Salvador', '202536', 1, 'armando.salvador@email.com', '', '2026-02-18', 1, 0),
(39, 'Consuelo Manalo', '202537', 1, 'consuelo.manalo@email.com', '', '2026-02-18', 2, 0),
(40, 'Roberto Sarmiento', '202538', 1, 'roberto.sarmiento@email.com', '', '2026-02-18', 0, 0),
(41, 'Milagros Paredes', '202539', 2, 'milagros.paredes@email.com', '', '2026-02-18', 0, 0),
(42, 'Renato Lacsamana', '202540', 1, 'renato.lacsamana@email.com', '', '2026-02-18', 0, 0),
(43, 'Elena Versoza', '202541', 1, 'elena.versoza@email.com', '', '2026-02-18', 0, 0),
(44, 'Mario Lacson', '202542', 1, 'mario.lacson@email.com', '', '2026-02-18', 0, 0),
(45, 'Natividad Bautista', '202543', 2, 'natividad.bautista@email.com', '', '2026-02-18', 0, 0),
(46, 'Danilo Mercado', '202544', 1, 'danilo.mercado@email.com', '', '2026-02-18', 0, 0),
(47, 'Leticia Valdez', '202545', 2, 'leticia.valdez@email.com', '', '2026-02-18', 0, 0),
(48, 'Gregorio Samson', '202546', 1, 'gregorio.samson@email.com', '', '2026-02-18', 1, 0),
(49, 'Virginia Adriano', '202547', 1, 'virginia.adriano@email.com', '', '2026-02-18', 1, 0),
(50, 'Rogelio Dizon', '202548', 1, 'rogelio.dizon@email.com', '', '2026-02-18', 1, 0),
(51, 'Evelyn Macapagal', '202549', 2, 'evelyn.macapagal@email.com', '', '2026-02-18', 0, 0),
(52, 'Teodoro Pascual', '202550', 1, 'teodoro.pascual@email.com', '', '2026-02-18', 0, 0),
(53, 'Aurora Cabrera', '202551', 2, 'aurora.cabrera@email.com', '', '2026-02-18', 0, 0),
(54, 'Leandro Trinidad', '202552', 1, 'leandro.trinidad@email.com', '', '2026-02-18', 0, 0),
(55, 'Belinda Marquez', '202553', 1, 'belinda.marquez@email.com', '', '2026-02-18', 0, 0),
(56, 'Cesar Velasco', '202554', 1, 'cesar.velasco@email.com', '', '2026-02-18', 0, 0),
(57, 'Imelda Javier', '202555', 2, 'imelda.javier@email.com', '', '2026-02-18', 0, 0),
(58, 'Wilfredo Aragon', '202556', 1, 'wilfredo.aragon@email.com', '', '2026-02-18', 0, 0),
(59, 'Violeta Delos Santos', '202557', 2, 'violeta.delossantos@email.com', '', '2026-02-18', 0, 0),
(60, 'Federico Bartolome', '202558', 1, 'federico.bartolome@email.com', '', '2026-02-18', 0, 0),
(61, 'Lourdes Sison', '202559', 1, 'lourdes.sison@email.com', '', '2026-02-18', 0, 0),
(62, 'Jaime Mendoza', '202560', 1, 'jaime.mendoza@email.com', '', '2026-02-18', 1, 0),
(63, 'Estrella Manansala', '202561', 2, 'estrella.manansala@email.com', '', '2026-02-18', 0, 0),
(64, 'Bernardo Lucas', '202562', 1, 'bernardo.lucas@email.com', '', '2026-02-18', 1, 0),
(65, 'Rosario Eusebio', '202563', 1, 'rosario.eusebio@email.com', '', '2026-02-18', 1, 0),
(66, 'Rolando Agbayani', '202564', 1, 'rolando.agbayani@email.com', '', '2026-02-18', 2, 0),
(67, 'Lilian Gonzales', '202565', 2, 'lilian.gonzales@email.com', '', '2026-02-18', 0, 0),
(68, 'Efren Guinto', '202566', 1, 'efren.guinto@email.com', '', '2026-02-18', 0, 0),
(69, 'Corazon Villegas', '202567', 2, 'corazon.villegas@email.com', '', '2026-02-18', 0, 0),
(71, 'Myrna Ducusin', '202569', 1, 'myrna.ducusin@email.com', '', '2026-02-18', 0, 0),
(72, 'Reynaldo Landicho', '202570', 1, 'reynaldo.landicho@email.com', '', '2026-02-18', 0, 0),
(73, 'Rosalinda Cabangon', '202571', 2, 'rosalinda.cabangon@email.com', '', '2026-02-18', 0, 0),
(74, 'Rustico Espiritu', '202572', 1, 'rustico.espiritu@email.com', '', '2026-02-18', 0, 0),
(75, 'Nieves Salamanca', '202573', 2, 'nieves.salamanca@email.com', '', '2026-02-18', 0, 0),
(76, 'Celso Peña', '202574', 1, 'celso.pena@email.com', '', '2026-02-18', 0, 0),
(77, 'Jovita Lagman', '202575', 1, 'jovita.lagman@email.com', '', '2026-02-18', 1, 0),
(78, 'Marcelo Silverio', '202576', 1, 'marcelo.silverio@email.com', '', '2026-02-18', 0, 0),
(79, 'Zenaida Abad', '202577', 2, 'zenaida.abad@email.com', '', '2026-02-18', 0, 0),
(80, 'Florencio Bautista', '202578', 1, 'florencio.bautista@email.com', '', '2026-02-18', 0, 0),
(81, 'Luz Garcia', '202579', 2, 'luz.garcia@email.com', '', '2026-02-18', 0, 0),
(82, 'Ramoncito Mariano', '202580', 1, 'ramoncito.mariano@email.com', '', '2026-02-18', 0, 0),
(83, 'Fe Salazar', '202581', 1, 'fe.salazar@email.com', '', '2026-02-18', 0, 0),
(84, 'Cipriano Mallari', '202582', 1, 'cipriano.mallari@email.com', '', '2026-02-18', 0, 0),
(85, 'Remedios Tolentino', '202583', 2, 'remedios.tolentino@email.com', '', '2026-02-18', 0, 0),
(86, 'Isidro Cruz', '202584', 1, 'isidro.cruz@email.com', '', '2026-02-18', 0, 0),
(87, 'Apolonia Ramirez', '202585', 1, 'apolonia.ramirez@email.com', '', '2026-02-18', 0, 0),
(88, 'Froilan Viray', '202586', 1, 'froilan.viray@email.com', '', '2026-02-18', 0, 0),
(89, 'Marilou Pascual', '202587', 2, 'marilou.pascual@email.com', '', '2026-02-18', 1, 0),
(90, 'Eduardo Rivera', '202588', 1, 'eduardo.rivera@email.com', '', '2026-02-18', 0, 0),
(91, 'Nora Aunor', '202589', 2, 'nora.aunor@email.com', '', '2026-02-18', 0, 0),
(92, 'Rogelio Mangubat', '202590', 1, 'rogelio.mangubat@email.com', '', '2026-02-18', 0, 0),
(93, 'Editha Fernandez', '202591', 1, 'editha.fernandez@email.com', '', '2026-02-18', 0, 0),
(94, 'Alejandro Layug', '202592', 1, 'alejandro.layug@email.com', '', '2026-02-18', 0, 0),
(95, 'Salvacion Imperial', '202593', 2, 'salvacion.imperial@email.com', '', '2026-02-18', 0, 0),
(96, 'Tomas Bernardo', '202594', 1, 'tomas.bernardo@email.com', '', '2026-02-18', 4, 0),
(97, 'Angelita Capili', '202595', 2, 'angelita.capili@email.com', '', '2026-02-18', 3, 0),
(98, 'Rodolfo Galang', '202596', 1, 'rodolfo.galang@email.com', '', '2026-02-18', 2, 0),
(99, 'Perlita Jacinto', '202597', 1, 'perlita.jacinto@email.com', '', '2026-02-18', 1, 0),
(100, 'Nicanor Reyes', '202598', 1, 'nicanor.reyes@email.com', '', '2026-02-18', 1, 0),
(101, 'Lilia Vda. de Castro', '202599', 2, 'lilia.castro@email.com', '', '2026-02-18', 0, 0),
(102, 'Crispin Martinez', '202600', 1, 'crispin.martinez@email.com', '', '2026-02-18', 0, 0),
(104, 'Maximo Quintos', '202602', 1, 'maximo.quintos@email.com', '', '2026-02-18', 0, 0),
(105, 'Visitacion Mabuhay', '202603', 2, 'visitacion.mabuhay@email.com', '', '2026-02-18', 0, 0),
(106, 'Silverio Navarro', '202604', 1, 'silverio.navarro@email.com', '', '2026-02-18', 0, 0),
(107, 'Benjamin Alonzo', '202605', 1, 'benjamin.alonzo@email.com', '', '2026-02-18', 0, 0),
(108, 'Felicidad Mateo', '202606', 2, 'felicidad.mateo@email.com', '', '2026-02-18', 0, 0),
(109, 'Lamberto Cunanan', '202607', 1, 'lamberto.cunanan@email.com', '', '2026-02-18', 0, 0),
(110, 'Pilar Vibar', '202608', 1, 'pilar.vibar@email.com', '', '2026-02-18', 0, 0),
(111, 'Romeo Tangco', '202609', 2, 'romeo.tangco@email.com', '', '2026-02-18', 0, 0),
(112, 'Susan Sempio', '202610', 1, 'susan.sempio@email.com', '', '2026-02-18', 0, 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adminacc_code`
--
ALTER TABLE `adminacc_code`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `access_code` (`access_code`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `borrow_records`
--
ALTER TABLE `borrow_records`
  ADD PRIMARY KEY (`id`),
  ADD KEY `member_id` (`member_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `member_id` (`member_id`),
  ADD KEY `category_id` (`category_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adminacc_code`
--
ALTER TABLE `adminacc_code`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `borrow_records`
--
ALTER TABLE `borrow_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=113;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `borrow_records`
--
ALTER TABLE `borrow_records`
  ADD CONSTRAINT `borrow_records_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `users` (`member_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `borrow_records_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
