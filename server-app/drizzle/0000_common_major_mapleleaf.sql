CREATE TABLE `community_comments` (
	`id` text PRIMARY KEY NOT NULL,
	`post_id` text,
	`author_id` text,
	`body` text NOT NULL,
	`created_at` text NOT NULL,
	FOREIGN KEY (`post_id`) REFERENCES `community_posts`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`author_id`) REFERENCES `community_profiles`(`user_id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE INDEX `community_comments_post` ON `community_comments` (`post_id`,`created_at`);--> statement-breakpoint
CREATE TABLE `community_likes` (
	`post_id` text,
	`user_id` text,
	`created_at` text NOT NULL,
	PRIMARY KEY(`post_id`, `user_id`),
	FOREIGN KEY (`post_id`) REFERENCES `community_posts`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`user_id`) REFERENCES `community_profiles`(`user_id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `community_posts` (
	`id` text PRIMARY KEY NOT NULL,
	`author_id` text,
	`title` text NOT NULL,
	`body` text NOT NULL,
	`topic` text DEFAULT '观察' NOT NULL,
	`city` text,
	`museum_id` text,
	`route_json` text,
	`status` text DEFAULT 'published' NOT NULL,
	`created_at` text NOT NULL,
	`updated_at` text NOT NULL,
	FOREIGN KEY (`author_id`) REFERENCES `community_profiles`(`user_id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE INDEX `community_posts_created` ON `community_posts` (`created_at`);--> statement-breakpoint
CREATE INDEX `community_posts_city` ON `community_posts` (`city`);--> statement-breakpoint
CREATE TABLE `community_profiles` (
	`user_id` text PRIMARY KEY NOT NULL,
	`nickname` text NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `community_reports` (
	`id` text PRIMARY KEY NOT NULL,
	`post_id` text,
	`reporter_id` text,
	`reason` text NOT NULL,
	`status` text DEFAULT 'pending' NOT NULL,
	`created_at` text NOT NULL,
	FOREIGN KEY (`post_id`) REFERENCES `community_posts`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`reporter_id`) REFERENCES `community_profiles`(`user_id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `community_report_unique` ON `community_reports` (`post_id`,`reporter_id`);